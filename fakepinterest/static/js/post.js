function init() {
  

    let search_bar = document.querySelector(".search_bar");
    let pagina = document.querySelector(".pagina");
    let janela_pastas = document.querySelector(".janela_pasta");
    let botao_pastas = document.querySelector(".botao_escolher_pasta");
    let janela_criar_pasta = document.querySelector(".janela_criar_pasta");
    let botao_criar_pasta = document.querySelector(".criar_pasta");

    
    
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
            console.log('fechado');
            janela_pastas.style.display = 'none';
    }};
    
    botao_criar_pasta.onclick = function(){
        janela_criar_pasta.style.display = "block";
        pagina.classList.toggle("inativo");
        janela_pastas.style.display = "none";
    };

    botao_pastas.onclick = function(){
        console.log('oi');
        janela_pastas.style.display = "block";
    };
    
}