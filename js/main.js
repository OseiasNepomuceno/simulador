// main.js - scripts gerais COREGOV

document.addEventListener('DOMContentLoaded', () => {
  // ===== HEADER SCROLL =====
  const header = document.querySelector('header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });

  // ===== SUPABASE CLIENT =====
  const supabaseClient = supabase.createClient(
    'https://mztdxodzbwbgtwbelltc.supabase.co',   // URL do projeto
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'     // chave anon
  );

  // ===== FORMULÁRIO DE CURRÍCULO =====
  const form = document.getElementById('curriculoForm');
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const nome = form.nome.value;
      const email = form.email.value;
      const telefone = form.telefone.value;
      const area = form.area.value;
      const experiencia = form.experiencia.value;
      const file = form.curriculo.files[0];

      let filePath = null;

      // Upload do arquivo
      if (file) {
        const safeFileName = file.name
          .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
          .replace(/\s+/g, "_")
          .replace(/[^a-zA-Z0-9._-]/g, "");

        const filePathKey = `uploads/${Date.now()}_${safeFileName}`;

        const { data: fileData, error: fileError } = await supabaseClient
          .storage
          .from('curriculos')
          .upload(filePathKey, file);

        if (fileError) {
          alert('Erro ao enviar arquivo: ' + fileError.message);
          return;
        } else {
          filePath = fileData.path;
        }
      }

      // Inserção dos dados
      const { error } = await supabaseClient
        .from('candidatos')
        .insert([{ nome, email, telefone, area, experiencia, curriculo: filePath }]);

      if (error) {
        alert('Erro ao salvar candidato: ' + error.message);
      } else {
        const dataLocal = new Date().toLocaleString("pt-BR", { timeZone: "America/Sao_Paulo" });
        alert(`Currículo enviado com sucesso!\nHorário BR: ${dataLocal}`);
        form.reset();
      }
    });
  }

  // ===== PAINEL ADMINISTRATIVO =====
  const lista = document.getElementById('listaCandidatos');
  const filtro = document.getElementById('filtro');

  async function carregarCandidatos(areaFiltro = "") {
    if (!lista) return;

    let query = supabaseClient.from('candidatos').select('*').order('id', { ascending: false });
    if (areaFiltro) query = query.eq('area', areaFiltro);

    const { data, error } = await query;

    if (error) {
      lista.innerHTML = `<tr><td colspan="6">Erro: ${error.message}</td></tr>`;
      return;
    }

    if (!data || data.length === 0) {
      lista.innerHTML = '<tr><td colspan="6">Nenhum candidato encontrado.</td></tr>';
      return;
    }

    lista.innerHTML = data.map(c => {
      const criadoEm = c.created_at
        ? new Date(c.created_at).toLocaleString("pt-BR", { timeZone: "America/Sao_Paulo" })
        : "—";

      return `
        <tr>
          <td>${c.nome}</td>
          <td>${c.email}</td>
          <td>${c.area}</td>
          <td>${c.telefone}</td>
          <td>${c.curriculo ? `<a href="https://mztdxodzbwbgtwbelltc.supabase.co/storage/v1/object/public/curriculos/${c.curriculo}" target="_blank">Download</a>` : "—"}</td>
          <td>${criadoEm}</td>
        </tr>
      `;
    }).join('');
  }

  if (lista) {
    carregarCandidatos();
    if (filtro) {
      filtro.addEventListener('change', () => carregarCandidatos(filtro.value));
    }
  }
});
