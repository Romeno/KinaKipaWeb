// nav.classList.toggle('is-opened');

// nav = document.getElementsByTagName('nav')[0]
// but = document.getElementsByClassName('hamburger')[0]

var showSearch = function() {
    nav = document.getElementsByTagName('nav')[0]
    nav.classList.toggle('is-opened')
    
    ul = nav.children[0]
    ul.classList.toggle('hidden')
    
    search_field = document.getElementsByClassName('search')[0]
    search_field.classList.toggle('visible')
    
    button = document.getElementsByClassName('search-button')[0]
    icon = button.getElementsByClassName('fa')[0]
    icon.classList.toggle('fa-search')
    icon.classList.toggle('fa-times')
}
