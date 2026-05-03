// ===============================
// 🔐 SISTEMA DE LOGIN + TRIAL
// ===============================

const TRIAL_DIAS = 3;

// Verifica usuário ao carregar página
window.addEventListener("load", async () => {
  await verificarUsuario();
});

async function verificarUsuario() {

  let usuario = localStorage.getItem("coregov_user");

  // 🧠 1. SE NÃO EXISTE → CRIA AUTOMÁTICO
  if (!usuario) {

    let novoUsuario = {
      id: crypto.randomUUID(),
      criado_em: new Date().toISOString(),
      trial_inicio: new Date().toISOString(),
      plano: "free"
    };

    localStorage.setItem("coregov_user", JSON.stringify(novoUsuario));

    // salva no supabase
    await supabaseClient.from("usuarios").insert([novoUsuario]);

    console.log("Novo usuário criado:", novoUsuario);

    return;
  }

  usuario = JSON.parse(usuario);

  // 🧠 2. VERIFICA TRIAL
  let inicio = new Date(usuario.trial_inicio);
  let hoje = new Date();

  let dias = (hoje - inicio) / (1000 * 60 * 60 * 24);

  if (dias > TRIAL_DIAS && usuario.plano !== "pro") {

    bloquearSistema();
  } else {
    console.log("Acesso liberado (trial ou pro)");
  }
}

// ===============================
// 🔒 BLOQUEIO
// ===============================
function bloquearSistema() {

  document.body.innerHTML = `
    <div style="
      display:flex;
      align-items:center;
      justify-content:center;
      height:100vh;
      background:#0B1220;
      color:white;
      text-align:center;
      padding:20px;
      font-family:Poppins;
    ">
      <div>
        <h2>🔒 Acesso expirado</h2>
        <p style="color:#ccc;">
          Seu período gratuito terminou.<br>
          Libere o acesso PRO para continuar usando as ferramentas.
        </p>

        <a href="https://wa.me/5518991511523?text=Quero acesso PRO CoreGov"
           style="
             display:inline-block;
             margin-top:15px;
             background:#00FF9F;
             color:#000;
             padding:12px 20px;
             border-radius:8px;
             text-decoration:none;
             font-weight:bold;
           ">
           Liberar acesso PRO
        </a>
      </div>
    </div>
  `;
}

// ===============================
// 🚀 FUNÇÃO FUTURA (PAGAMENTO)
// ===============================
function liberarPro() {

  let usuario = JSON.parse(localStorage.getItem("coregov_user"));
  usuario.plano = "pro";

  localStorage.setItem("coregov_user", JSON.stringify(usuario));

  location.reload();
}
