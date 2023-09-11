function init() {
  

    let search_bar = document.querySelector(".search_bar");
    let pagina = document.querySelector(".pagina");
    let janela_pastas = document.querySelector(".janela_pasta");
    let botao_pastas = document.querySelector(".botao_escolher_pasta");
    let janela_criar_pasta = document.querySelector(".janela_criar_pasta");
    let botao_criar_pasta = document.querySelector(".criar_pasta");
    let janela_editar_foto = document.querySelector(".janela_editar_foto");
    let botao_editar_foto = document.querySelector(".botao_editar_foto");
    let menu_header = document.querySelector(".dropdown_menu");
    let seta_header = document.querySelector(".seta_header");

    
    
    pagina.onclick = function(e){
        if (!search_bar.contains(e.target)) {
            if (search_bar.value !="") {
                search_bar.value = ""
            }}
        if (janela_criar_pasta.style.display == "block" && !janela_criar_pasta.contains(e.target) && !criar_pasta.contains(e.target)){
            pagina.classList.remove("inativo");
            janela_criar_pasta.style.display = "none";
            }
        if (janela_pastas.style.display==='block' && !janela_pastas.contains(e.target) && !botao_pastas.contains(e.target)){
            janela_pastas.style.display = 'none';}

        if (janela_editar_foto.style.display==='block' && !janela_editar_foto.contains(e.target) && !botao_editar_foto.contains(e.target)){
            pagina.classList.remove("inativo");
            janela_editar_foto.style.display = 'none';}
        if (menu_header.style.display == "block" && !menu_header.contains(e.target) && !seta_header.contains(e.target)){
            menu_header.style.display = "none";
        }   
        };
    
    botao_criar_pasta.onclick = function(){
        janela_criar_pasta.style.display = "block";
        pagina.classList.toggle("inativo");
        janela_pastas.style.display = "none";
    };

    botao_editar_foto.onclick = function(){
        janela_editar_foto.style.display = "block";
        pagina.classList.toggle("inativo");
    };

    botao_pastas.onclick = function(){
        janela_pastas.style.display = "block";
    };
    seta_header.onclick = function(){
        menu_header.style.display = "block";
    };
    
}