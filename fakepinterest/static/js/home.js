let botao_login = document.querySelector(".botao_login_header")
let botao_cadastrar = document.querySelector(".botao_cadastrar_header")
let pagina = document.querySelector(".container")
let janela_login = document.querySelector(".janela_login")
let janela_cadastro = document.querySelector(".janela_cadastro")

if(janela_login.classList.contains("aberto") || janela_cadastro.classList.contains("aberto")){
        pagina.classList.toggle("inativo")
        }

botao_login.onclick = function(){
        if(!janela_cadastro.classList.contains("aberto")){
        janela_login.classList.toggle("aberto")
        pagina.classList.toggle("inativo")
        }
}
botao_cadastrar.onclick = function(){
        if(!janela_login.classList.contains("aberto")){
        janela_cadastro.classList.toggle("aberto")
        pagina.classList.toggle("inativo")
        }
}
pagina.onclick = function(e){
if (janela_login.classList.contains("aberto") && !botao_login.contains(e.target)
    && !janela_login.contains(e.target) && !botao_cadastrar.contains(e.target)) {
pagina.classList.remove("inativo");
janela_login.classList.remove("aberto");
}if (janela_cadastro.classList.contains("aberto") && !botao_cadastrar.contains(e.target)
    && !janela_cadastro.contains(e.target) && !botao_login.contains(e.target)) {
pagina.classList.remove("inativo");
janela_cadastro.classList.remove("aberto");
}                
}