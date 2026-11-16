
document.addEventListener("DOMContentLoaded", function () {
    const botao = document.getElementById("alternar-contraste");

    if (!botao) return;

    function atualizarBotao(ativado) {
        document.body.classList.toggle("alto-contraste", ativado);

        botao.setAttribute("aria-pressed", String(ativado));

        botao.textContent = ativado
            ? "Alto contraste: ligado"
            : "Alto contraste: desligado";
    }

    const contrasteSalvo =
        localStorage.getItem("altoContraste") === "ativado";

    atualizarBotao(contrasteSalvo);

    botao.addEventListener("click", function () {
        const ativado =
            !document.body.classList.contains("alto-contraste");

        localStorage.setItem(
            "altoContraste",
            ativado ? "ativado" : "desativado"
        );

        atualizarBotao(ativado);
    });
});
