import urllib
import ftplib
import os
import tempfile

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from datetime import date
from django.conf import settings

from .utils import remove_cache, check_post, GenericRequest, clean_inputs, ResponseDic, send_server_error, send_server_forbidden

from django.contrib.auth import authenticate, login, logout

from django.core.context_processors import csrf
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.contrib.auth.models import User

from django.http import HttpResponse

from django.template.loader import get_template
from django.template import Context, RequestContext

from django.shortcuts import render_to_response, get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import utc

from userprofile.models import UserProfile, QRCodeSignups, UserQRCode, UserSettings
from challenges.models import Challenge, UserChallenge,  ChallengeQRCode
from cleanteams.models import CleanTeam, CleanTeamMember, CleanTeamPost, CleanChampion, CleanTeamInvite, CleanTeamLevel
from notifications.models import UserNotification

import json,urlparse,random,string, base64,datetime

#@remove_cache
#@check_post
def logout_user(request):
	response_base = ResponseDic()
	
	logout(request)
	response_base.response['status'] = 1

	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	return HttpResponse(data, mimetype="text/javascript")

#@remove_cache
#@check_post
@csrf_exempt
def login_user(request):
    request_obj = GenericRequest(request)
    request_obj.parse_request_params()
    response_base = ResponseDic()
    inputs = ["username", "password"]
    cleaned_inputs = clean_inputs(request_obj.params, inputs, inputs)
    if cleaned_inputs:
        return send_server_error(cleaned_inputs)
    #print request_obj.params
    try:
        user = authenticate(username=request_obj.params['username'], password=request_obj.params["password"])
		
        if user:
			role=""
			cleanteamname =""
			cleanteamid=""
			try:
				#role = user.cleanteammember_set.values_list('role',flat=True).get()
				role_array    = CleanTeamMember.objects.get(user_id=user.id,status="approved")
				role  = role_array.role
		
			except Exception,e:
				print e
				try:
					champarray = CleanChampion.objects.get(user_id=user.id)
					role = "clean-champion"
				except Exception,e:
					print e
					role = "Individual"
		
			try:
				cleanteamid  = user.cleanteammember_set.values_list('clean_team_id',flat=True).get()
				cleanteamArray  = CleanTeam.objects.get(id=cleanteamid)
				cleanteamname  = cleanteamArray.name
			except Exception,e:
				print e
				cleanteamname =""
			qr_code_array = UserQRCode.objects.get(user_id=user.id)	
			response_base.response['data'] = {'userid': user.id, 'status': 1,'role':role,'qrcode':unicode(qr_code_array.qr_image),'team':cleanteamname,'ctid':cleanteamid}
			login(request_obj.http_request, user)
        else:
            response_base.response['status'] = 0
    except Exception, e:
        print e
        response_base.response['status'] = 0
        
    #return HttpResponse(response_base.send_json_response(), "application/json")
    #print response_base.response
    data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
    return HttpResponse(data, mimetype="text/javascript")

#@remove_cache
#@check_post
@csrf_exempt
def registration(request):
	#print '*'*30
    request_obj = GenericRequest(request)
    request_obj.parse_request_params()
    response_base = ResponseDic()
    inputs = []#"firstname", "lastname", "email", "password", "city", "province", "school_type"]
    #cleaned_inputs = clean_inputs(request_obj.params, inputs, inputs)
    #print cleaned_inputs
    #if cleaned_inputs:
    #return send_server_error(cleaned_inputs)
    params = request_obj.params
    #print params
    try:
	u = User.objects.create_user(
			params['email'],
			params['email'],
			params['password']
		)

	u.first_name = params['firstname']
	u.last_name = params['lastname']
	u.profile.city = params['city']
	u.profile.province = params['province']
	u.profile.school_type = params['school_type']
	u.profile.save()
	u.save()
	

    #if 'qrcode' in self.kwargs:
        qr_code_signup = QRCodeSignups()
        qr_code_signup.user = User.objects.latest('id')
        qr_code_signup.save()

	#user = authenticate(username=u.username, password=params['password'])
	#login(request, user)

	# Send registration email to user
	template = get_template('emails/user_register_success.html')
	content = Context({ 'first_name': params['firstname'] })
	content = template.render(content)

	subject, from_email, to = 'My Clean City - Signup Successful', 'info@mycleancity.org', params['email']

	mail = EmailMessage(subject, content, from_email, [to])
	mail.content_subtype = "html"
	# mail.send()

	# Send notification email to administrator
	template = get_template('emails/register_email_notification.html')
	content = Context({ 'email': params['email'], 'first_name': params['firstname'], 'last_name': params['lastname'], 'student': 'student' })
	content = template.render(content)

	subject, from_email, to = 'My Clean City - Student Signup Successful', 'info@mycleancity.org', 'communications@mycleancity.org'

	mail = EmailMessage(subject, content, from_email, [to])
	mail.content_subtype = "html"
	# mail.send()
	qr_code_array = UserQRCode.objects.get(user_id=u.id)
	#print qr_code_array.qr_image
	response_base.response['data'] = {'userid': u.id,'qrcode':unicode(qr_code_array.qr_image)}

	#print response_base.send_json_response()
	#return HttpResponse(response_base.send_json_response(), mimetype="application/json", status=200, content_type="application/json")
    except:
	response_base.response['status'] = 0
	response_base.response['errorMessages'] = 'Invalid'
	
    data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response)) 
    return HttpResponse(data, mimetype="text/javascript")

def qrcode(request):
	request_obj = GenericRequest(request)
	request_obj.parse_request_params()
	response_base = ResponseDic()

	user = request.user

	try:
		qr_code = UserQRCode.objects.get(user=user)
	except Exception, e:
		qr_code = None

	qr_code = unicode(qr_code.qr_image)
	
	response_base.response['data'] = {'qrcode':qr_code}
	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	
	return HttpResponse(data, mimetype="text/javascript")

def edit_user_profile(request):
	if request.is_ajax:
		request_obj = GenericRequest(request)
		request_obj.parse_request_params()
		response_base = ResponseDic()

		user = request.user
		
		user.first_name = request_obj.params['first_name']
		user.last_name = request_obj.params['last_name']
		user.email = request_obj.params['email']
		user.save()

		user.profile.about = request_obj.params['about']
		user.profile.twitter = request_obj.params['twitter']

		user.profile.save()

	response_base.response['status'] = 1
	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	
	return HttpResponse(data, mimetype="text/javascript")

def get_user_profile(request):
	request_obj = GenericRequest(request)
	request_obj.parse_request_params()
	response_base = ResponseDic()

	if 'userid' in request_obj.params:
		userid = request_obj.params['userid']
		user = User.objects.get(id=userid)
	else:
		user = request.user

	user_profile = user.profile	
	total_hours = user_profile.get_total_hours()

	role = ""
	cleanteamname = ""
	cleanteamid = ""

	try:
		role_array = CleanTeamMember.objects.get(user_id=request_obj.params['userid'],status="approved")
		role  = role_array.role
		role = "clean-ambassador"
		
	except Exception,e:
		if user_profile.is_clean_champion():
			role = "clean-champion"
		else:
			role = "individual"
		
	try:
		cleanteamid = user.cleanteammember_set.values_list('clean_team_id', flat=True).get()
		cleanteamArray = CleanTeam.objects.get(id=cleanteamid)
		cleanteamname = cleanteamArray.name
	except Exception, e:
		cleanteamname = ""

	picture = unicode(user_profile.picture)
	
	response_base.response['data'] = {
		'email':user.email,
		'firstname': user.first_name,
		'lastname':user.last_name,
		'twitter':user_profile.twitter,
		'city':user_profile.city,
		'cleancreds':user_profile.clean_creds, 
		'totalhours': total_hours, 
		'school':user_profile.school_type,
		'about':user_profile.about,
		'role':role,
		'team':cleanteamname,
		'picture':picture
	}
	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	
	return HttpResponse(data, mimetype="text/javascript")

def update_user(request):
	request_obj = GenericRequest(request)
	request_obj.parse_request_params()
	response_base = ResponseDic()
	user_profile = UserProfile.objects.get(user_id=request_obj.params['userid'])
	user = User.objects.get(id=request_obj.params['userid'])
	user_profile.twitter = request_obj.params['twitter']
	user_profile.about = request_obj.params['about']
	user_profile.school_type = "test"
	user.email = request_obj.params['email']
	user.first_name = request_obj.params['firstname']
	user.last_name = request_obj.params['lastname']
	user.save()
	user_profile.save()
	response_base.response['status'] = 1
	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	return HttpResponse(data, mimetype="text/javascript")

def get_challenge(request):
	request_obj = GenericRequest(request)
	request_obj.parse_request_params()
	response_base = ResponseDic()
		
	challenge_id = request_obj.params['cid']
	challenge_json = []
	participants_json = []
	user_challenge_json = []

	try:
		challenge = Challenge.objects.get(id=challenge_id)

		challenge_json = {
			'id':challenge.id, 
			'title':challenge.title, 
			'eventstartdate':str(challenge.event_start_date),
			'eventstarttime':str(challenge.event_start_time),
			'eventenddate':str(challenge.event_end_date),
			'eventendtime':str(challenge.event_end_time),
			'address1':challenge.address1,
			'address2':challenge.address2,
			'city':challenge.city,
			'province':challenge.province,
			'postalcode':challenge.postal_code,
			'country':challenge.country,
			'description':challenge.description,
			'userid':challenge.user.id,
			'cleanteamid':challenge.clean_team.id,
			'cleanteamname':challenge.clean_team.name,
			'cleancredsperhour':challenge.clean_creds_per_hour,
			'nationalchallenge':challenge.national_challenge,
			'type':challenge.type.challenge_type,
			'organization':challenge.organization,
			'contactfirstname':challenge.contact_first_name,
			'contactlastname':challenge.contact_last_name,
			'contactphone':challenge.contact_phone,
			'contactemail':challenge.contact_email
		}
	except Exception, e:
		print e
		response_base.response['status'] = 0
	
	try:
		user_challenge = UserChallenge.objects.get(challenge=challenge, user=request.user)

		user_challenge_json = {
			'id':user_challenge.id,
			'timestamp':str(user_challenge.timestamp),
			'time_in':str(user_challenge.time_in),
			'time_out':str(user_challenge.time_out),
			'total_hours':user_challenge.total_hours,
			'total_clean_creds':user_challenge.total_clean_creds
		}
	except Exception, e:
		print e

	try:
		participants = UserChallenge.objects.raw("SELECT id, user_id FROM challenges_userchallenge WHERE challenge_id = %s GROUP BY user_id, challenge_id" % (challenge_id))

		for participant in participants:
			u = participant.user

			if u.profile.picture:
				picture = u.profile.picture
			else:
				picture = 0
		
			participants_json.append({
				'uid':u.id,
				'pic':unicode(picture),
				'firstname':u.first_name,
				'lastname':u.last_name
			})
	
		response_base.response['status'] = 1
	except Exception, e:
		print e
		response_base.response['status'] = 0

	response_base.response['user_challenge_data'] = user_challenge_json
	response_base.response['participants_data'] = participants_json
	response_base.response['data'] = challenge_json
	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	
	return HttpResponse(data, mimetype="text/javascript")

def list_challenge(request):
    #print "#"*30
	request_obj = GenericRequest(request)
	request_obj.parse_request_params()
	response_base = ResponseDic()
	user_id=request_obj.params['userid']
		
	#print user_id
	try:
		#ctm = CleanTeamMember.objects.get(user_id=user_id, role="clean-ambassador", status="approved")
		#challenge = Challenge.objects.filter(clean_team_id=ctm.clean_team_id)
		#print "ctm.clean_team_id",ctm.clean_team_id
		#print chanllege
		#print ', '.join(challenge)
		query = ""
		national_challenges = "false"
		challenge = Challenge.search_challenges(query, national_challenges)
		jsonvalue = []

		for each in challenge:
			ct_id = each.clean_team_id
			qr_id = each.qr_code_id
			if qr_id:
				try:
					#print "&"*30
					qrarray = ChallengeQRCode.objects.get(id=qr_id)
					#print unicode(qrarray.qr_image)
					qrimage = unicode(qrarray.qr_image)
				except Exception,e:
					print e
					qrimage = ""
			else:
				qrimage = ""
			cteamarray  = CleanTeam.objects.get(id=ct_id)
			ctname  = cteamarray.name
			org = each.host_organization
			jsonvalue.append({'country':each.country
			,'ctname':ctname
			,'title':each.title
			,'address1':each.address1
			,'address2':each.address2
			,'postal_code':each.postal_code
			,'city':each.city
			,'eventdate':str(each.event_start_date)
			,'eventtime':str(each.event_start_time)
			,'province':each.province,'id':each.id
			,'description':each.description
			,'clean_creds_per_hour':each.clean_creds_per_hour
			,'type_id':each.type_id
			,'qr_code':qrimage})
		
		response_base.response['status'] = 1
		#challenges = {"adress":challenge.title}
		#response_base.response['data'] = [ {'title':each.title,'org':each.host_organization,'city':each.city,'eventdate':str(each.event_date),'eventtime':str(each.event_time),'province':each.province,'id':each.id,'description':each.description} for each in challenge]
		response_base.response['data'] = jsonvalue
	except Exception,e:
		print e
		response_base.response['status'] = 0
  	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	return HttpResponse(data, mimetype="text/javascript")

def list_participants(request):
	request_obj = GenericRequest(request)
	request_obj.parse_request_params()
	response_base = ResponseDic()

	cid = request_obj.params['challenge_id']
	participants = UserChallenge.objects.raw("SELECT id, user_id, challenge_id, max(time_in) AS time_in FROM challenges_userchallenge WHERE challenge_id = %s GROUP BY user_id, challenge_id" % (cid))

	jsonvalue = []
	challenge_json = []

	try:
		challenge = Challenge.objects.get(id=cid)

		challenge_json = {
			'id':challenge.id, 
			'title':challenge.title, 
			'eventstartdate':str(challenge.event_start_date),
			'eventstarttime':str(challenge.event_start_time),
			'eventenddate':str(challenge.event_end_date),
			'eventendtime':str(challenge.event_end_time),
			'address1':challenge.address1,
			'address2':challenge.address2,
			'city':challenge.city,
			'province':challenge.province,
			'postalcode':challenge.postal_code,
			'country':challenge.country,
			'description':challenge.description,
			'userid':challenge.user.id,
			'cleanteamid':challenge.clean_team.id,
			'cleanteamname':challenge.clean_team.name,
			'cleancredsperhour':challenge.clean_creds_per_hour,
			'nationalchallenge':challenge.national_challenge,
			'type':challenge.type.challenge_type,
			'organization':challenge.organization,
			'contactfirstname':challenge.contact_first_name,
			'contactlastname':challenge.contact_last_name,
			'contactphone':challenge.contact_phone,
			'contactemail':challenge.contact_email
		}
	except Exception, e:
		print e
		response_base.response['status'] = 0

	for each in participants:
		challenge = each.challenge
		type = challenge.type.challenge_type
		time_in = str(each.time_in)
		time_out = str(each.time_out)
		hours = each.total_hours
		total_clean_creds = each.total_clean_creds

		if time_in != 'None':
			time_in = str(datetime.datetime.strptime(str(time_in)[:19], "%Y-%m-%d %H:%M:%S"))

		if time_out != 'None':
			time_out = str(datetime.datetime.strptime(str(time_out)[:19], "%Y-%m-%d %H:%M:%S"))
		
		jsonvalue.append({
			'hours':hours,
			'totalcleancreds':total_clean_creds,
			'type':type,
			'timein':time_in,
			'timeout':time_out,
			'userid':each.user_id,
			'hours':each.total_hours,
			'firstname':each.user.first_name,
			'lastname':each.user.last_name
		})

	response_base.response['status'] = 1
	response_base.response['data'] = jsonvalue	
	response_base.response['challenge_data'] = challenge_json	
	
	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	return HttpResponse(data, mimetype="text/javascript")

def add_cleanteam(request):
	#print "*"*30
    request_obj = GenericRequest(request)
    request_obj.parse_request_params()
    response_base = ResponseDic()
    ct = CleanTeam()
    ctm = CleanTeamMember()
    profile = UserProfile()
    userid = request_obj.params['userid']	
    ct.name = request_obj.params['team_name']
    ct.region = request_obj.params['team_region']
    ct.website = request_obj.params['team_website']
    ct.twitter = request_obj.params['team_twitter']
    ct.about  = request_obj.params['team_about']
    ct.team_type = request_obj.params['team_type']
    ct.group = request_obj.params['team_group_name']
    #data = ct.save()
    try:
        lid = ct.save()
        last_inserted = CleanTeam.objects.order_by('-id')[0]
        #print last_inserted.id 
        team_id = last_inserted.id
        ctm.clean_team_id = team_id
        ctm.user_id = userid
        ctm.status = "approved"
        ctm.role = "clean-ambassador"
        ctm.save()
        user = User.objects.get(id=userid)
        #id = user.cleanteammember_set.values_list('id',flat=True).get()
        ctmArray = CleanTeamMember.objects.get(user_id = user)
        #print "edwin",ctmArray.id
        user.profile.clean_team_member = ctmArray
        user.profile.save()
        #print "edwin",id
        """user_profile = UserProfile.objects.get(user_id=userid)
        user_profile.clean_team_member_id = id
        user_profile.save()"""
        response_base.response['status'] = 1
    except Exception, e:
        #print e
        response_base.response['status'] = 0        	
    data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
    return HttpResponse(data, mimetype="text/javascript")
def list_team(request):
    teams = CleanTeam.objects.all()
    response_base = ResponseDic()
    response_base.response['status'] = 1	
    response_base.response['data']= [ {'id':each.id,'name':each.name} for each in teams ]
    data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
    return HttpResponse(data, mimetype="text/javascript")
def join_team(request):
    request_obj = GenericRequest(request)
    request_obj.parse_request_params()
    response_base = ResponseDic()
    ctm = CleanTeamMember()
    ctm.user_id = request_obj.params['userid']
    ctm.clean_team_id  = request_obj.params['teamid']
    ctm.role = "clean-ambassador"
    ctm.status = "pending"	
    if ctm.user_id:
        ctm.save()
        response_base.response['status'] = 1
    else:
        response_base.response['status'] = 0
    data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
    return HttpResponse(data, mimetype="text/javascript")

def invite_user(request):
    request_obj = GenericRequest(request)
    request_obj.parse_request_params()
    response_base = ResponseDic()
    userid = request_obj.params['userid']
    try:
        ctm = CleanTeamMember.objects.get(user_id=userid, role="clean-ambassador", status="approved")
        #user = request.user
        cleanteam_id = ctm.clean_team_id
        #print cleanteam_id
        email = request_obj.params['email']
        role  = request_obj.params['role']
        uri  = request.build_absolute_uri()
        uriParsed = urlparse.urlparse(uri)
        scheme = uriParsed[0]
        domain = uriParsed[1]
        fullPath = "%s://%s/clean-teams/invite/"%(scheme,domain)
        invite = CleanTeamInvite()
        invite.inviteUsersNew(cleanteam_id,userid, role, email, fullPath)
        response_base.response['status'] = 1
    except CleanTeamMember.DoesNotExist:
        response_base.response['status'] = 0	
    data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
    return HttpResponse(data, mimetype="text/javascript")
def pending_list(request):
    request_obj = GenericRequest(request)
    request_obj.parse_request_params()
    response_base = ResponseDic()
    userid = request_obj.params['userid']
    pendinglist = CleanTeamInvite.objects.filter(user_id=userid,status="pending")
    response_base.response['status'] = 1	
    response_base.response['data']= [ {'email':each.email,'status':each.status} for each in pendinglist ]
    data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
    return HttpResponse(data, mimetype="text/javascript")
def approved_list(request):
    request_obj = GenericRequest(request)
    request_obj.parse_request_params()
    response_base = ResponseDic()
    userid = request_obj.params['userid']
    pendinglist = CleanTeamInvite.objects.filter(user_id=userid,status="approved")
    response_base.response['status'] = 1	
    response_base.response['data']= [ {'email':each.email,'status':each.status} for each in pendinglist ]
    data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
    return HttpResponse(data, mimetype="text/javascript")
def joinchampion_team(request):
    request_obj = GenericRequest(request)
    request_obj.parse_request_params()
    response_base = ResponseDic()
    userid = request_obj.params['userid']
    team   = request_obj.params['teamid']
    user = User.objects.get(id=userid)
    cc = CleanChampion()
    cc.becomeCleanChampionNew(user,userid, team)
    """ctm.user_id = request_obj.params['userid']
    ctm.clean_team_id  = request_obj.params['teamid']
    ctm.role = "clean-ambassador"
    ctm.status = "pending"	
    if ctm.user_id:
        ctm.save()
        response_base.response['status'] = 1
    else:
        response_base.response['status'] = 0"""
    response_base.response['status'] = 1	
    data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
    return HttpResponse(data, mimetype="text/javascript")

def list_notification(request):
    request_obj = GenericRequest(request)
    request_obj.parse_request_params()
    response_base = ResponseDic()
    user = request.user

    try:
		un = UserNotification.objects.filter(user=user).order_by('-timestamp')
		uncount = UserNotification.objects.filter(user=user,read=0).order_by('-timestamp').count()
		response_base.response['data']= [ {'message':each.message,'datetime':str(each.timestamp),'read':each.read,'id':each.id} for each in un ]
		response_base.response['status'] = 1
		response_base.response['count'] = uncount
    except Exception,e:
        print e
        response_base.response['status'] = 0
    
    data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
    
    return HttpResponse(data, mimetype="text/javascript")

def count_notification(request):
    request_obj = GenericRequest(request)
    request_obj.parse_request_params()
    response_base = ResponseDic()
    userid = request_obj.params['userid']
    try:
        uncount = UserNotification.objects.filter(user=userid).order_by('-timestamp').count()
        #print uncount
        response_base.response['data']= {'count':uncount}
        response_base.response['status'] = 1
    except Exception,e:
        print e
        response_base.response['status'] = 0
    data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
    return HttpResponse(data, mimetype="text/javascript")	
@csrf_exempt	
def upload_picture(request):
	print "@"*30
	request_obj = GenericRequest(request)
	request_obj.parse_request_params()
	response_base = ResponseDic()
	
	picture   = request.FILES['file'].read()
	filename= request.FILES['file'].name
	print filename
	filenamearray = filename.split('.')
	#print filenamearray[0]
	user = User.objects.get(id=filenamearray[0])
	"""
	path="E:\\uploads\\%s"%filename
	f=open(path,'wb')
	f.write(picture)
	f.close()
	
	return HttpResponse('test')"""
	
	if picture:			
		conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
		bucket = conn.get_bucket(settings.AWS_BUCKET)
		k = Key(bucket)
		k.key = 'uploads/user_picture_%s_%s' % (str(user.id), filename)
		#k.key = 'uploads/user_picture_test'
		k.set_contents_from_string(picture)
		user.profile.picture = k.key

	user.profile.save()
	
	response_base.response['status'] = 1
	data = [{"status":"1"}]
	return HttpResponse(data, mimetype="text/javascript")
def view_participants(request):
	request_obj = GenericRequest(request)
	request_obj.parse_request_params()
	response_base = ResponseDic()
	chid = request_obj.params['chid']
	challenge = UserChallenge.objects.filter(challenge_id=chid)
	jsonvalue =[]
	for each in challenge:		
		userid = each.user_id
		#print user_id
		uprofilearray  = UserProfile.objects.get(user_id=userid)
		picture  = uprofilearray.picture
		if picture:
			picture = picture
		else:
			picture =0
		Userid = uprofilearray.user_id
		userarray  = User.objects.get(id=Userid)
		uname   =  userarray.first_name
		jsonvalue.append({'pic':unicode(picture),'firstname':uname,'uid':Userid})
	#print jsonvalue
	response_base.response['status'] = 1
	response_base.response['data'] = jsonvalue
	#response_base.response['data'] = [ {'title':each.user_id} for each in challenge]
	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	return HttpResponse(data, mimetype="text/javascript")
def qrcode_userchallenge(request):
	request_obj = GenericRequest(request)
	request_obj.parse_request_params()
	response_base = ResponseDic()
	uc  = UserChallenge()
	now = datetime.datetime.now()
	try:
		uc.user_id = request_obj.params['userid']
		uc.challenge_id = request_obj.params['challengeid']
		uc.save()
		response_base.response['status'] = 1
	except Exception,e:
		print e
		response_base.response['status'] = 0
		
	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	return HttpResponse(data, mimetype="text/javascript")
def my_challenge(request):
	request_obj = GenericRequest(request)
	request_obj.parse_request_params()
	response_base = ResponseDic()
	user = request.user

	try:
		Uchallenge = UserChallenge.objects.filter(user=user)
		jsonvalue = []

		for each in Uchallenge:		
			challengeid = each.challenge_id
			ChallengesInstance  = each.challenge
			CTeam  = ChallengesInstance.clean_team
			ctname     = CTeam.name
			
			challengearray  = Challenge.objects.get(id=challengeid)
			qr_id = challengearray.qr_code_id

			if qr_id:
				try:
					qrarray = ChallengeQRCode.objects.get(id=qr_id)
					qrimage = unicode(qrarray.qr_image)
				except Exception,e:
					print e
					qrimage = ""
			else:
				qrimage = ""

			time_in = each.time_in
			time_out = each.time_out

			if time_in != None:
				time_in = str(datetime.datetime.strptime(str(time_in)[:19], "%Y-%m-%d %H:%M:%S"))

			if time_out != None:
				time_out = str(datetime.datetime.strptime(str(time_out)[:19], "%Y-%m-%d %H:%M:%S"))

			jsonvalue.append({
				'title':challengearray.title
				,'description':challengearray.description
				,'event_date':str(challengearray.event_start_date)
				,'event_time':str(challengearray.event_start_time)
				,'id':challengearray.id
				,'address1':challengearray.address1
				,'address2':challengearray.address2
				,'city':challengearray.city
				,'ctname':ctname
				,'province':challengearray.province
				,'postal_code':challengearray.postal_code
				,'country':challengearray.country
				,'organization':challengearray.organization
				,'contact_first_name':challengearray.contact_first_name
				,'contact_last_name':challengearray.contact_last_name
				,'contact_phone':challengearray.contact_phone
				,'contact_email':challengearray.contact_email
				,'cleanperhour':challengearray.clean_creds_per_hour
				,'total_hours':each.total_hours
				,'total_clean_creds':each.total_clean_creds
				,'time_in':time_in
				,'time_out':time_out
				,'type_id':challengearray.type_id
				,'qr_code':qrimage
				,'last_updated_by_id':challengearray.last_updated_by_id
			})

		response_base.response['status'] = 1
		response_base.response['teamstatus'] = 0
		response_base.response['data'] = jsonvalue	
		response_base.response['totalhours'] = user.profile.get_total_hours()	
	except Exception,e:
		print e
		response_base.response['status'] = 0
	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	return HttpResponse(data, mimetype="text/javascript")	

def check_in_check_out(request):
	if request.is_ajax:
		request_obj = GenericRequest(request)
		request_obj.parse_request_params()
		response_base = ResponseDic()

		user = request.user
		cid = request_obj.params['cid']
		uid = request_obj.params['uid']

		challenge = get_object_or_404(Challenge, id=cid)
		response = challenge.check_in_check_out(uid)

		if response:
			response_base.response['html'] = response
			response_base.response['status'] = 1
		else:
			response_base.response['status'] = 0

	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	
	return HttpResponse(data, mimetype="text/javascript")

def check_in(request):
	request_obj = GenericRequest(request)
	request_obj.parse_request_params()
	response_base = ResponseDic()
	try:
		user_challenge = UserChallenge.objects.get(user_id=request_obj.params['userid'],challenge_id=request_obj.params['challengeid'])
		user = user_challenge.user
		challenge = user_challenge.challenge
		cleancredaperhour = challenge.clean_creds_per_hour
		#print challenge
		time_in = user_challenge.time_in
		if time_in:
			now = datetime.datetime.utcnow().replace(tzinfo=utc)
			timediff = (now -  time_in).total_seconds()
			hours = timediff // 3600
			user_challenge.time_out = now
			user_challenge.total_hours = hours
			total_clean_creds  = hours*cleancredaperhour
			user_challenge.total_clean_creds = total_clean_creds
			user_challenge.save()
			
			
			# Add CleanCreds to individual
			user.profile.add_clean_creds(total_clean_creds)

			# Add CleanCreds to Clean Teams if applicable
			clean_champions = CleanChampion.objects.filter(user=user)

			for clean_champion in clean_champions:
				if clean_champion.status == "approved":
					clean_champion.clean_team.add_team_clean_creds(total_clean_creds)
					
			# Clean Ambassador
			if user.profile.is_clean_ambassador():
				user.profile.clean_team_member.clean_team.add_team_clean_creds(total_clean_creds)
			
			# Clean Team posting challenge	
			challenge.clean_team.add_team_clean_creds(total_clean_creds)
			response_base.response['status'] = 1
			response_base.response['hours'] = hours
			response_base.response['total_clean_creds'] = total_clean_creds
		else:	
			now = datetime.datetime.now()
			user_challenge.time_in = now
			user_challenge.save()
			response_base.response['status'] = 1
	except Exception,e:
		print e
		response_base.response['status'] = 0
	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	return HttpResponse(data, mimetype="text/javascript")

def check_out(request):
	request_obj = GenericRequest(request)
	request_obj.parse_request_params()
	response_base = ResponseDic()
	try:
		user_challenge = UserChallenge.objects.get(user_id=request_obj.params['userid'],challenge_id=request_obj.params['challengeid'])
		time_in = user_challenge.time_in
		#newtimein = datetime.datetime(time_in)
		#print newtimein
		now = datetime.datetime.utcnow().replace(tzinfo=utc)
		#now = datetime.datetime.now()
		#timediff = datetime.datetime.utcnow().replace(tzinfo=utc) - time_in
		timediff = (now -  time_in).total_seconds()
		#print timediff
		#print sec = timediff.days
		hours = timediff // 3600
		#print hours
		user_challenge.time_out = now
		user_challenge.total_hours = hours
		user_challenge.total_clean_creds = hours*10
		user_challenge.save()
		response_base.response['status'] = 1
	except Exception,e:
		print e
		response_base.response['status'] = 0
	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	return HttpResponse(data, mimetype="text/javascript")
	
def search(request):
	request_obj = GenericRequest(request)
	request_obj.parse_request_params()
	response_base = ResponseDic()

	query = request_obj.params['q']
	national_challenges = request_obj.params['national_challenges']

	if national_challenges == "0":
		national_challenges = "false"
	else:	
		national_challenges = "true"
	
	#print national_challenges	
	
	challenges = Challenge.search_challenges(query, national_challenges, 10)
	print challenges
	
	if challenges:
		jsonvalue = []

		for each in challenges:
			ct_id = each.clean_team_id
			cteamarray  = CleanTeam.objects.get(id=ct_id)
			ctname  = cteamarray.name

			qr_id = each.qr_code_id

			if qr_id:
				try:
					#print "&"*30
					qrarray = ChallengeQRCode.objects.get(id=qr_id)
					#print unicode(qrarray.qr_image)
					qrimage = unicode(qrarray.qr_image)
				except Exception,e:
					print e
					qrimage = ""
			else:
				qrimage = ""

			jsonvalue.append({
				'country':each.country
				,'ctname':ctname
				,'title':each.title
				,'address1':each.address1
				,'address2':each.address2
				,'postal_code':each.postal_code
				,'city':each.city
				,'eventdate':str(each.event_start_date)
				,'eventtime':str(each.event_start_time)
				,'province':each.province,'id':each.id
				,'description':each.description
				,'clean_creds_per_hour':each.clean_creds_per_hour
				,'type_id':each.type_id
			})
		
		response_base.response['status'] = 1
	else:
		response_base.response['status'] = 0
	
	response_base.response['data'] = jsonvalue
	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	
	return HttpResponse(data, mimetype="text/javascript")		

def make_me_read(request):
	request_obj = GenericRequest(request)
	request_obj.parse_request_params()
	response_base = ResponseDic()
	notid = request_obj.params['notid']
	usernotification = 	UserNotification.objects.get(id=notid)
	usernotification.read =1
	usernotification.save()
	response_base.response['status'] = 1
	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	return HttpResponse(data, mimetype="text/javascript")

def participate_challenge(request):
	if request.is_ajax:
		request_obj = GenericRequest(request)
		request_obj.parse_request_params()
		response_base = ResponseDic()

		user = request.user
		cid = request_obj.params['cid']
		challenge = Challenge.objects.get(id=cid)

		try:
			user_challenge = UserChallenge.objects.get(user=user, challenge=challenge)
		except Exception, e:
			user_challenge = UserChallenge(user=request.user)
			user_challenge.challenge = challenge
			user_challenge.save()

	response_base.response['status'] = 1
	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	
	return HttpResponse(data, mimetype="text/javascript")

def onetime_ch(request):
	request_obj = GenericRequest(request)
	request_obj.parse_request_params()
	response_base = ResponseDic()
	userid = request_obj.params['userid']
	cid = request_obj.params['cid']
	token = request_obj.params['token']
	#print userid
	#print cid
	try:
		challenge = Challenge.objects.get(id=cid, token=token)

		#user = request.user
		user = User.objects.get(id=userid)
		userchallenge, created = UserChallenge.objects.get_or_create(user=user, challenge_id=cid)
		challenge = userchallenge.challenge

		now = datetime.datetime.utcnow().replace(tzinfo=utc)
		total_clean_creds = challenge.clean_creds_per_hour

		userchallenge.time_in = now
		userchallenge.time_out = now
		userchallenge.total_hours = 0
		userchallenge.total_clean_creds = total_clean_creds
		userchallenge.save()

		# Add CleanCreds to individual
		user.profile.add_clean_creds(total_clean_creds)

		# Add CleanCreds to Clean Teams if applicable
		clean_champions = CleanChampion.objects.filter(user=user)

		for clean_champion in clean_champions:
			if clean_champion.status == "approved":
				clean_champion.clean_team.add_team_clean_creds(total_clean_creds)
				
		# Clean Ambassador
		if user.profile.is_clean_ambassador():
			user.profile.clean_team_member.clean_team.add_team_clean_creds(total_clean_creds)
		
		# Clean Team posting challenge	
		challenge.clean_team.add_team_clean_creds(total_clean_creds)
	except Exception, e:
		print e
	response_base.response['status'] = 1
	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	return HttpResponse(data, mimetype="text/javascript")
def newsfeeds(request):
	#print "@"*30
	request_obj = GenericRequest(request)
	request_obj.parse_request_params()
	response_base = ResponseDic()
	user_id=request_obj.params['userid']
	limitcount=request_obj.params['limitcount']	
	#print limitcount
	#print user_id
	try:
		#ctm = CleanTeamMember.objects.get(user_id=user_id, role="clean-ambassador", status="approved")
		#challenge = Challenge.objects.filter(clean_team_id=ctm.clean_team_id)
		#print "ctm.clean_team_id",ctm.clean_team_id
		#print chanllege
		#print ', '.join(challenge)
		query = ""
		#print limit
		national_challenges = ""
		if limitcount == "1":
			challenge = Challenge.search_challenges(query, national_challenges)
		else:
			challenge = Challenge.search_challenges(query, national_challenges,10)
		
		jsonvalue =[]
		for each in challenge:
			ct_id = each.clean_team_id
			qr_id = each.qr_code_id
			if qr_id:
				try:
					#print "&"*30
					qrarray = ChallengeQRCode.objects.get(id=qr_id)
					#print unicode(qrarray.qr_image)
					qrimage = unicode(qrarray.qr_image)
				except Exception,e:
					print e
					qrimage = ""
			else:
				qrimage = ""
			cteamarray  = CleanTeam.objects.get(id=ct_id)
			ctname  = cteamarray.name
			org = each.host_organization
			jsonvalue.append({'country':each.country
			,'ctname':ctname
			,'title':each.title
			,'org':each.host_organization
			,'address1':each.address1
			,'address2':each.address2
			,'postal_code':each.postal_code
			,'city':each.city
			,'eventdate':str(each.event_start_date)
			,'eventtime':str(each.event_start_time)
			,'province':each.province,'id':each.id
			,'description':each.description
			,'clean_creds_per_hour':each.clean_creds_per_hour
			,'type_id':each.type_id
			,'qr_code':qrimage})
		
		response_base.response['status'] = 1
		#challenges = {"adress":challenge.title}
		#response_base.response['data'] = [ {'title':each.title,'org':each.host_organization,'city':each.city,'eventdate':str(each.event_date),'eventtime':str(each.event_time),'province':each.province,'id':each.id,'description':each.description} for each in challenge]
		response_base.response['data'] = jsonvalue
	except Exception,e:
		print e
		response_base.response['status'] = 0
  	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	return HttpResponse(data, mimetype="text/javascript")
def cleanteam_view(request):
	request_obj = GenericRequest(request)
	request_obj.parse_request_params()
	response_base = ResponseDic()
	try:
		ctarray = CleanTeam.objects.get(id=request_obj.params['ctid'])
		level_id  = ctarray.level_id
		ctlarray = CleanTeamLevel.objects.get(id=level_id)
		badge  = unicode(ctlarray.badge)
		
		response_base.response['status'] = 1
		response_base.response['data'] = {'name': ctarray.name, 'website': ctarray.website,'logo':unicode(ctarray.logo),'clean_creds':ctarray.clean_creds,'about':ctarray.about,'twitter':ctarray.twitter,'region':ctarray.region,'team_type':ctarray.team_type,'badge':badge}	
		
		try:
			challengePost = CleanTeamPost.objects.filter(clean_team_id=request_obj.params['ctid'])
			jsonvalue =[]
			for each in challengePost:
				userid = each.user_id
				user = User.objects.get(id=userid)
				jsonvalue.append({'timedate':str(each.timestamp)
				,'message':each.message
				,'firstname':user.first_name
				,'lastname':user.last_name})
			response_base.response['postdata'] = jsonvalue	
		except Exception,e:	
			response_base.response['status'] = 0
	except Exception,e:
		print e
		response_base.response['status'] = 0
	
	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	return HttpResponse(data, mimetype="text/javascript")

def team_challenge(request):
	request_obj = GenericRequest(request)
	request_obj.parse_request_params()
	response_base = ResponseDic()

	user = request.user
	clean_team = request.user.profile.clean_team_member.clean_team
	
	try:
		challenge = Challenge.objects.filter(clean_team=clean_team)
		jsonvalue =[]
		for each in challenge:		
			#challengeid = each.challenge_id
			#challengearray  = Challenge.objects.get(id=challengeid)
			qr_id = each.qr_code_id
			if qr_id:
				try:
					#print "&"*30
					qrarray = ChallengeQRCode.objects.get(id=qr_id)
					#print unicode(qrarray.qr_image)
					qrimage = unicode(qrarray.qr_image)
				except Exception,e:
					print e
					qrimage = ""
			else:
				qrimage = ""
			jsonvalue.append({'title':each.title
			,'description':each.description
			,'id':each.id
			,'address1':each.address1
			,'address2':each.address2
			,'city':each.city
			,'province':each.province
			,'postal_code':each.postal_code
			,'country':each.country
			,'cleanperhour':each.clean_creds_per_hour
			,'nationalchallenges':each.national_challenge
			,'total_hours':"0"
			,'total_clean_creds':"0"
			,'time_in':"0"
			,'time_out':"0"
			,'type_id':each.type_id
			,'qr_code':qrimage})	
		response_base.response['status'] = 1
		response_base.response['teamstatus'] = 1
		response_base.response['data'] = jsonvalue	
	except Exception,e:
		print e
		response_base.response['status'] = 0
	data = '%s(%s);' % (request.REQUEST['callback'], json.dumps(response_base.response))
	return HttpResponse(data, mimetype="text/javascript")	