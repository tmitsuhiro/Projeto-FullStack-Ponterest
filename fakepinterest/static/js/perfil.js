window.addEventListener('load', function () {
  

let search_bar = document.querySelector(".search_bar");
let pagina = document.querySelector(".pagina");
let botao_criar_pasta = document.querySelector(".botao_plus_div");
let janela_criar_pasta = document.querySelector(".janela_criar_pasta");
let menu_header = document.querySelector(".dropdown_menu");
let seta_header = document.querySelector(".seta_header");
let image = document.querySelector(".imagem_foto"),
    input = document.querySelector(".input_foto"),
    botao_editar_foto_perfil = document.querySelector(".botao_editar_foto_perfil"),
    botao_cancelar = document.querySelector(".botao_cancelar"),
    janela_foto_perfil = document.querySelector(".janela_foto_perfil");

    input.addEventListener("change", () => {
        image.src = URL.createObjectURL(input.files[0]);

    });



    pagina.onclick = function(e){
    if (!search_bar.contains(e.target)) {
        if (search_bar.value !="") {
        search_bar.value = ""
        }
    }if (janela_criar_pasta.classList.contains("aberto") && !janela_criar_pasta.contains(e.target) && !botao_criar_pasta.contains(e.target)){
        pagina.classList.remove("inativo");
        janela_criar_pasta.classList.remove("aberto");
    }if (menu_header.style.display == "block" && !menu_header.contains(e.target) && !seta_header.contains(e.target)){
        menu_header.style.display = "none";
    }if (janela_foto_perfil.style.display == "block" && !janela_foto_perfil.contains(e.target) && !botao_editar_foto_perfil.contains(e.target)){
        janela_foto_perfil.style.display = "none";
        pagina.classList.remove("inativo");
    }      
};


botao_criar_pasta.onclick = function(e){
    janela_criar_pasta.classList.toggle("aberto");
    pagina.classList.toggle("inativo");
};
botao_editar_foto_perfil.onclick = function(e){
    janela_foto_perfil.style.display = "block"
    pagina.classList.toggle("inativo");
};
botao_cancelar.onclick = function(e){
    janela_foto_perfil.style.display = "none"
    pagina.classList.remove("inativo");
};
seta_header.onclick = function(){
    menu_header.style.display = "block";
};

})