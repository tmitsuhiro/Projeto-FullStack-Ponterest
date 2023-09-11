function init() {
    let search_bar = document.querySelector(".search_bar");
    let menu_header = document.querySelector(".dropdown_menu");
    let seta_header = document.querySelector(".seta_header");
    let pagina = document.querySelector("body");


    pagina.onclick = function(e){
        if (!search_bar.contains(e.target)) {
            if (search_bar.value !="") {
                search_bar.value = ""
            }}
        if (menu_header.style.display == "block" && !menu_header.contains(e.target) && !seta_header.contains(e.target)){
            menu_header.style.display = "none";
            console.log("pag")
        }   
        };
    
    seta_header.onclick = function(){
        menu_header.style.display = "block";
    };
    
}