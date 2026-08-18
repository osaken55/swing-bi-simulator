/**
 * TSH Beyond-Dashboard Executive Gatekeeper Auth (Zero Side-Effect)
 * Password: tsh2026
 */
(function() {
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

  window.tshLogout = function() {
    sessionStorage.removeItem('tsh_auth_token');
    window.location.reload();
  };

  function initGatekeeper() {
    if (isAuthorized()) return;

    // 単体の独立オーバーレイ（既存DOM・CSSに一切影響を与えない）
    const overlay = document.createElement('div');
    overlay.id = 'tsh-gatekeeper-overlay';
    overlay.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;background:#070a0f;z-index:9999999;display:flex;align-items:center;justify-content:center;font-family:-apple-system,BlinkMacSystemFont,sans-serif;color:#f8fafc;padding:16px;box-sizing:border-box;';
    overlay.innerHTML = `
      <div style="background:#0d1522;border:1px solid rgba(56,189,248,0.3);box-shadow:0 24px 64px rgba(0,0,0,0.8),0 0 32px rgba(56,189,248,0.15);border-radius:16px;width:100%;max-width:420px;padding:32px 28px;text-align:center;box-sizing:border-box;">
        <div style="display:inline-flex;align-items:center;gap:6px;background:rgba(201,169,97,0.15);color:#C9A961;border:1px solid rgba(201,169,97,0.35);padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;margin-bottom:16px;">🔒 TSH関係者様 限定アクセス</div>
        <div style="font-size:19px;font-weight:800;margin-bottom:6px;letter-spacing:-0.3px;">TSH Beyond-Dashboard</div>
        <div style="font-size:13px;color:#94a3b8;line-height:1.6;margin-bottom:24px;">
          本環境は東京システムハウス様向け先行検証プレビューです。<br>
          閲覧パスコードを入力してください。
        </div>
        <form id="tsh-auth-form" onsubmit="return false;">
          <div style="margin-bottom:16px;">
            <input type="password" id="tsh-auth-input" placeholder="パスコードを入力" autofocus style="width:100%;background:#141f30;border:1.5px solid #223247;border-radius:10px;padding:12px 16px;color:#fff;font-size:15px;outline:none;box-sizing:border-box;text-align:center;letter-spacing:2px;">
          </div>
          <button type="submit" style="width:100%;background:linear-gradient(135deg,#0284c7 0%,#0369a1 100%);border:1px solid #38bdf8;color:#fff;font-size:14.5px;font-weight:700;padding:12px;border-radius:10px;cursor:pointer;box-shadow:0 4px 14px rgba(2,132,199,0.4);">ロック解除して閲覧</button>
          <div id="tsh-auth-err" style="color:#f87171;font-size:12.5px;font-weight:600;margin-top:12px;display:none;">⚠️ パスコードが正しくありません</div>
        </form>
      </div>
    `;
    document.body.appendChild(overlay);

    const form = document.getElementById('tsh-auth-form');
    const input = document.getElementById('tsh-auth-input');
    const err = document.getElementById('tsh-auth-err');

    async function tryAuth() {
      const val = input.value.trim();
      if (!val) return;
      const hash = await sha256(val);
      if (hash === TARGET_HASH || val === "tsh2026") {
        setAuthorized();
        overlay.style.opacity = '0';
        overlay.style.transition = 'opacity 0.2s ease';
        setTimeout(() => overlay.remove(), 200);
      } else {
        err.style.display = 'block';
        input.value = '';
        input.focus();
      }
    }

    form.addEventListener('submit', tryAuth);
    setTimeout(() => { if (input) input.focus(); }, 100);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGatekeeper);
  } else {
    initGatekeeper();
  }
})();
