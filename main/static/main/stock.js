document.addEventListener('DOMContentLoaded', () => {
	document.querySelector('.info').style.display = 'none';
})

function show() {
	const info = document.querySelector('.info')

	if (info.style.display === 'none') {
		info.style.display = 'block';
	}

	else {
		info.style.display = 'none';
		}
};