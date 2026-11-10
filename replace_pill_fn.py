app_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    js = f.read()

idx1 = js.find('function updateHeaderUserPill() {')
idx2 = js.find('function openAccountModal() {', idx1)

if idx1 != -1 and idx2 != -1:
    old_fn = js[idx1:idx2]
    new_fn = '''function updateHeaderUserPill() {
  const pill = document.getElementById('header-user-btn');
  const avatar = document.getElementById('header-user-avatar');
  const nameEl = document.getElementById('header-user-name');
  const roleEl = document.getElementById('header-user-role');

  if (!pill) return;
  const user = (typeof getActiveAccount === 'function' ? getActiveAccount() : null) || STATE.currentUser || { name: 'Sinh Viên Y Khoa', role: 'student', username: 'ykhoa' };

  if (nameEl) nameEl.textContent = user.name || user.full_name || user.username;
  if (avatar) {
    avatar.textContent = user.avatar || (user.name || user.username || 'U')[0].toUpperCase();
  }
  if (roleEl) {
    if (user.role === 'admin') {
      roleEl.textContent = '👑 Quản Trị';
      roleEl.className = 'badge-rose px-1.5 py-0.5 rounded text-[10px] font-black';
    } else {
      roleEl.textContent = '🎓 ' + (user.name ? user.name.split('(')[0].trim() : 'Sinh Viên');
      roleEl.className = 'badge-brand px-1.5 py-0.5 rounded text-[10px] font-black text-emerald-400';
    }
  }
}

'''
    js = js[:idx1] + new_fn + js[idx2:]
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(js)
    print("Updated updateHeaderUserPill successfully!")
else:
    print("Could not find targets:", idx1, idx2)
