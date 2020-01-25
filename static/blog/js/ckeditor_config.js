/**
 * @license Copyright (c) 2003-2019, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here.
	// For complete reference see:
	// https://ckeditor.com/docs/ckeditor4/latest/api/CKEDITOR_config.html

	// The toolbar groups arrangement, optimized for two toolbar rows.
    config.language = 'en';
    config.extraPlugins = ['codesnippet', 'emoji'];
    config.toolbarGroups = [
        {name: 'basicstyles', groups: ['basicstyles']},
        {name: 'links'},
        {name: 'insert'},
        {name: 'others'},
    ];

    // The default plugins included in the basic setup define some buttons that
    // are not needed in a basic editor. They are removed here.
    config.removeButtons = 'Cut,Copy,Paste,Undo,Redo,Anchor,Underline,Strike,Subscript,Superscript,Image,Table    ';

    // Dialog windows are also simplified.
    config.removeDialogTabs = 'image:advanced;link:advanced';
};
