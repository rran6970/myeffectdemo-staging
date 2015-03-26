
    "use strict";

    // This is required for Yahoo's skins:
    if( window.YAHOO ) {
        YAHOO.util.Event.onDOMReady(function() { YAHOO.util.Dom.addClass(document.body, 'yui-skin-sam'); });
    }


    /*
        This config is used for our standard rich editor on the site and in the
        Django admin area if you've modified the change_form.html to enable
        rich editing.

        See Yahoo's documentation for customization options:

        http://developer.yahoo.com/yui/editor/
    */

    var django_wysiwyg_editor_configs = [];   // allow custom settings per editor ID

    var django_wysiwyg_editor_config = {
        height: "400px",
        width: "624px",
        animate: true,
        autoHeight: true,
        // BUG: handleSubmit breaks contrib.admin's save-and-continue-editing feature - we can avoid by listening for blur events
        // This will cause the rich editor to update the original textarea's value when the containing form submit event fires
        handleSubmit: true,
        focusAtStart: false,
        toolbar: {
            //collapse: true,
            //titlebar: 'Body',
            draggable: false,
            buttons: [
            {
                group: 'fontstyle',
                label: 'Font Name and Size',
                buttons: [
                    { type: 'select', label: 'Arial', value: 'fontname', disabled: true,
                      menu: [
                        { text: 'Arial', checked: true },
                        { text: 'Arial Black' },
                        { text: 'Comic Sans MS' },
                        { text: 'Courier New' },
                        { text: 'Georgia' },
                        { text: 'Impact' },
                        { text: 'Lucida Console' },
                        { text: 'Tahoma' },
                        { text: 'Times New Roman' },
                        { text: 'Trebuchet MS' },
                        { text: 'Verdana' }
                      ]
                    },
                    { type: 'spin', label: '13', value: 'fontsize', range: [9, 75], disabled: true }
                ]
            },
            {
                type: 'separator'
            },
            {
                group: 'textstyle',
                label: 'Font Style',
                buttons: [
                    { type: 'push', label: 'Bold CTRL + SHIFT + B', value: 'bold' },
                    { type: 'push', label: 'Italic CTRL + SHIFT + I', value: 'italic' },
                    { type: 'push', label: 'Underline CTRL + SHIFT + U', value: 'underline' },
                    { type: 'separator' },
                    { type: 'color', label: 'Font Color', value: 'forecolor', disabled: true },
                    { type: 'color', label: 'Background Color', value: 'backcolor', disabled: true }
                ]
            },
            {
                type: 'separator'
            },
            {
                group: 'indentlist',
                label: 'Lists',
                buttons: [
                    { type: 'push', label: 'Create an Unordered List', value: 'insertunorderedlist' },
                    { type: 'push', label: 'Create an Ordered List', value: 'insertorderedlist' }
                ]
            },
            {
                type: 'separator'
            },
            {
                group: 'insertitem',
                label: 'Insert Item',
                buttons: [
                    { type: 'push', label: 'HTML Link CTRL + SHIFT + L', value: 'createlink', disabled: true },
                    { type: 'push', label: 'Insert Image', value: 'insertimage' }
                ]
            }
            ]
        }
    };


    var django_wysiwyg =
    {
        editors: {},

        enable: function django_wysiwyg_enable(editor_name, field_id, config)
        {
            if( !config ) {
                config = django_wysiwyg_editor_configs[field_id] || django_wysiwyg_editor_config;
            }
            if( !this.editors[editor_name] ) {
              this.editors[editor_name] = new YAHOO.widget.Editor(field_id, config);
              this.editors[editor_name].render();
            }
        },

        disable: function django_wysiwyg_disable(editor_name)
        {
            var editor = this.editors[editor_name];
            if( editor ) {
                editor.saveHTML();
                editor.destroy();
                this.editors[editor_name] = null;
            }
        },

        is_loaded: function django_wysiwyg_is_loaded()
        {
          return window.YAHOO != null
              && window.YAHOO.widget != null
              && window.YAHOO.widget.Editor != null;
        }
    }
