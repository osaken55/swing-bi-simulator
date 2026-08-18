/**
 * TSH Beyond-Dashboard Executive Gatekeeper Auth
 * Password: tsh2026
 */
(function() {
  // パスワード "tsh2026" の SHA-256 ハッシュ値
  const TARGET_HASH = "8f31b674843bcf1489069dcf46fc09520a7b4570ffccf754a6dbb4458f2780e0";

  async function sha256(message) {
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

  function isAuthorized() {
    return sessionStorage.getItem('tsh_auth_token') === 'authorized_tsh_2026';
  }

  function setAuthorized() {
    sessionStorage.setItem('tsh_auth_token', 'authorized_tsh_2026');
  }

  function logout() {
    sessionStorage.removeItem('tsh_auth_token');
    window.location.reload();
  }

  window.tshLogout = logout;

  // 認証モーダルの注入
  function injectAuthUI() {
    if (isAuthorized()) {
      document.documentElement.classList.add('tsh-authenticated');
      return;
    }

    // 未認証時のスタイル
    const style = document.createElement('style');
    style.id = 'tsh-gatekeeper-style';
    style.textContent = `
      body:not(.tsh-authenticated-ready) > *:not(#tsh-gatekeeper-modal) {
        filter: blur(24px) brightness(0.2) !important;
        pointer-events: none !important;
        user-select: none !important;
      }
      #tsh-gatekeeper-modal {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(circle at center, rgba(14, 21, 32, 0.95) 0%, rgba(6, 9, 14, 0.98) 100%);
        backdrop-filter: blur(20px);
        z-index: 999999;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
        font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Noto Sans JP', sans-serif;
      }
      .gatekeeper-card {
        background: #0d1522;
        border: 1px solid rgba(56, 189, 248, 0.3);
        box-shadow: 0 24px 64px rgba(0, 0, 0, 0.8), 0 0 32px rgba(56, 189, 248, 0.15);
        border-radius: 16px;
        width: 100%;
        max-width: 440px;
        padding: 32px 28px;
        text-align: center;
        color: #f8fafc;
        animation: gatekeeper-in 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
      }
      @keyframes gatekeeper-in {
        from { opacity: 0; transform: scale(0.92) translateY(12px); }
        to { opacity: 1; transform: scale(1) translateY(0); }
      }
      .gatekeeper-card.shake {
        animation: gatekeeper-shake 0.4s ease;
      }
      @keyframes gatekeeper-shake {
        0%, 100% { transform: translateX(0); }
        20%, 60% { transform: translateX(-10px); }
        40%, 80% { transform: translateX(10px); }
      }
      .gatekeeper-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(201, 169, 97, 0.15);
        color: #C9A961;
        border: 1px solid rgba(201, 169, 97, 0.35);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 16px;
      }
      .gatekeeper-title {
        font-size: 19px;
        font-weight: 800;
        margin-bottom: 6px;
        letter-spacing: -0.3px;
      }
      .gatekeeper-desc {
        font-size: 13px;
        color: #94a3b8;
        line-height: 1.6;
        margin-bottom: 24px;
      }
      .gatekeeper-input-wrap {
        position: relative;
        margin-bottom: 16px;
      }
      .gatekeeper-input {
        width: 100%;
        background: #141f30;
        border: 1.5px solid #223247;
        border-radius: 10px;
        padding: 12px 16px;
        color: #fff;
        font-size: 15px;
        outline: none;
        box-sizing: border-box;
        text-align: center;
        letter-spacing: 2px;
        transition: all 0.2s ease;
      }
      .gatekeeper-input:focus {
        border-color: #38bdf8;
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.25);
      }
      .gatekeeper-btn {
        width: 100%;
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        border: 1px solid #38bdf8;
        color: #fff;
        font-size: 14.5px;
        font-weight: 700;
        padding: 12px;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.15s ease;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4);
      }
      .gatekeeper-btn:hover {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.5);
      }
      .gatekeeper-error {
        color: #f87171;
        font-size: 12.5px;
        font-weight: 600;
        margin-top: 12px;
        display: none;
      }
    `;
    document.head.appendChild(style);

    const modal = document.createElement('div');
    modal.id = 'tsh-gatekeeper-modal';
    modal.innerHTML = `
      <div class="gatekeeper-card" id="gatekeeper-card">
        <div class="gatekeeper-badge">🔒 TSH関係者様 限定アクセス</div>
        <div class="gatekeeper-title">TSH Beyond-Dashboard</div>
        <div class="gatekeeper-desc">
          本環境は東京システムハウス様向け先行検証プレビューです。<br>
          閲覧パスコードを入力してください。
        </div>
        <form id="gatekeeper-form" onsubmit="return false;">
          <div class="gatekeeper-input-wrap">
            <input type="password" id="gatekeeper-pass" class="gatekeeper-input" placeholder="パスコードを入力" autofocus autocomplete="current-password">
          </div>
          <button type="submit" id="gatekeeper-submit" class="gatekeeper-btn">ロック解除して閲覧</button>
          <div id="gatekeeper-err" class="gatekeeper-error">⚠️ パスコードが正しくありません</div>
        </form>
      </div>
    `;
    document.body.appendChild(modal);

    const form = document.getElementById('gatekeeper-form');
    const input = document.getElementById('gatekeeper-pass');
    const card = document.getElementById('gatekeeper-card');
    const err = document.getElementById('gatekeeper-err');

    async function handleAuth() {
      const val = input.value.trim();
      if (!val) return;
      const hash = await sha256(val);
      if (hash === TARGET_HASH || val === "tsh2026") {
        setAuthorized();
        modal.style.opacity = '0';
        modal.style.transition = 'opacity 0.25s ease';
        setTimeout(() => {
          modal.remove();
          document.body.classList.add('tsh-authenticated-ready');
          document.documentElement.classList.add('tsh-authenticated');
        }, 250);
      } else {
        card.classList.remove('shake');
        void card.offsetWidth; // reflow
        card.classList.add('shake');
        err.style.display = 'block';
        input.value = '';
        input.focus();
      }
    }

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      handleAuth();
    });

    setTimeout(() => { input.focus(); }, 100);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectAuthUI);
  } else {
    injectAuthUI();
  }
})();
