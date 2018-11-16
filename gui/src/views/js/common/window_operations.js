$ = require('jquery')
const {ipcRenderer, remote} = require('electron');


$('#close_window_button').on('click', ()=>{
	var current_window = remote.getCurrentWindow();
	current_window.close(); 
});

$('#minimize_window_button').on('click', ()=>{
	var current_window = remote.getCurrentWindow();
	current_window.minimize(); 
});


$('#finished-button').on('click', ()=>{
	var current_window = remote.getCurrentWindow();
	current_window.close(); 
});
