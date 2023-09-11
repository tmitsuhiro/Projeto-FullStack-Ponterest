window.addEventListener('load', function () {
  

let search_bar = document.querySelector(".search_bar");
let pagina = document.querySelector(".pagina");
let botao_criar_pasta = document.querySelector(".botao_plus_div");
let janela_criar_pasta = document.querySelector(".janela_criar_pasta");


pagina.onclick = function(e){
if (!search_bar.contains(e.target)) {
    if (search_bar.value !="") {
    search_bar.value = ""
    }
}if (janela_criar_pasta.classList.contains("aberto") && !janela_criar_pasta.contains(e.target) && !botao_criar_pasta.contains(e.target)){
    pagina.classList.remove("inativo");
    janela_criar_pasta.classList.remove("aberto");
    }   
};


botao_criar_pasta.onclick = function(e){
    janela_criar_pasta.classList.toggle("aberto");
    pagina.classList.toggle("inativo");
}

})