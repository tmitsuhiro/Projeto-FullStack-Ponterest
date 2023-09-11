function init() {
  

    let search_bar = document.querySelector(".search_bar");
    let pagina = document.querySelector(".pagina");
    let janela_editar_pasta = document.querySelector(".janela_editar_pasta");
    let botao_editar_pasta = document.querySelector(".botao_editar_pasta");
    let menu_header = document.querySelector(".dropdown_menu");
    let seta_header = document.querySelector(".seta_header");

    
    
    pagina.onclick = function(e){
        if (!search_bar.contains(e.target)) {
            if (search_bar.value !="") {
                search_bar.value = ""
            }}
        if (janela_editar_pasta.style.display == "block" && !janela_editar_pasta.contains(e.target) && !botao_editar_pasta.contains(e.target)){
            pagina.classList.remove("inativo");
            janela_editar_pasta.style.display = "none";
        }if (menu_header.style.display == "block" && !menu_header.contains(e.target) && !seta_header.contains(e.target)){
            menu_header.style.display = "none";
        }
    };
    
    botao_editar_pasta.onclick = function(){
        janela_editar_pasta.style.display = "block";
        pagina.classList.toggle("inativo");
    };
    seta_header.onclick = function(){
        menu_header.style.display = "block";
    };
    
}