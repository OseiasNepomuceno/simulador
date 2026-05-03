async function verificarAcesso() {

  let usuario = JSON.parse(localStorage.getItem("usuario"));

  // 🔹 Se não existe usuário → cria automaticamente
  if (!usuario) {

    const { data, error } = await supabaseClient
      .from("usuarios")
      .insert([
        {
          plano: "free",
          trial_inicio: new Date()
        }
      ])
      .select()
      .single();

    if (error) {
      console.error("Erro ao criar usuário:", error);
      return;
    }

    localStorage.setItem("usuario", JSON.stringify(data));
    console.log("Novo usuário criado:", data);

    return;
  }

  // 🔹 Já existe usuário
  let inicio = new Date(usuario.trial_inicio);
  let hoje = new Date();

  let diffDias = (hoje - inicio) / (1000 * 60 * 60 * 24);

  // 🔥 LIBERAÇÃO TOTAL
  if (usuario.plano === "pro") {
    console.log("Usuário PRO liberado");
    return;
  }

  // 🔥 TRIAL ATIVO
  if (diffDias <= 3) {
    console.log("Trial ativo:", diffDias.toFixed(1), "dias");
    return;
  }

  // 🔒 BLOQUEIO
  bloquearFerramenta();
}

function bloquearFerramenta() {

  document.body.innerHTML = `
    <div style="
      display:flex;
      justify-content:center;
      align-items:center;
      height:100vh;
      background:#0B1220;
      color:#fff;
      font-family:Poppins;
      text-align:center;
      padding:20px;
    ">
      <div>
        <h2>🔒 Acesso expirado</h2>
        <p style="color:#ccc;">
          Seu período gratuito terminou.<br>
          Libere o acesso completo PRO agora.
        </p>

        <a href="https://wa.me/5518991511523?text=Quero acesso PRO"
           style="
            display:inline-block;
            margin-top:20px;
            padding:12px 20px;
            background:#00FF9F;
            color:#000;
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

verificarAcesso();
