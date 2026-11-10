import os, re

app_js_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\app.js'
with open(app_js_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update DEFAULT_UI_PREFS
old_prefs = """const DEFAULT_UI_PREFS = {
  theme: 'dark', // 'dark' (Pure OLED #000) | 'light' | 'sepia'
  brand: '#7c3aed',
  brand2: '#ec4899',
  fontUi: "'Plus Jakarta Sans', sans-serif",
  fontQuestion: 'inherit',
  fontAnswer: 'inherit',
  fontCode: "'JetBrains Mono', monospace",
  baseFontPx: 16,
  qFontRem: 1.14,
  optFontRem: 1.02,
  soundEnabled: true,
  autoNext: false
};"""

new_prefs = """const DEFAULT_UI_PREFS = {
  theme: 'dark', // 'dark' (Pure OLED #000) | 'midnight' | 'contrast' | 'light' | 'sepia'
  brand: '#7c3aed',
  brand2: '#ec4899',
  fontUi: "'Plus Jakarta Sans', sans-serif",
  fontQuestion: 'inherit',
  fontAnswer: 'inherit',
  fontCode: "'JetBrains Mono', monospace",
  baseFontPx: 16,
  qFontRem: 1.14,
  optFontRem: 1.02,
  lineHeight: 1.62,
  cardRadiusPx: 18,
  shadowDepth: 'medium',
  soundEnabled: true,
  soundVolume: 0.8,
  ttsSpeed: 1.0,
  autoNext: false,
  autoNextDelaySec: 0.8,
  timerMode: 'countdown',
  antiCheatLevel: 'medium',
  defaultTutorPersona: 'professor',
  aiVerbosity: 'standard'
};"""

if old_prefs in text:
    text = text.replace(old_prefs, new_prefs, 1)
    print("Updated DEFAULT_UI_PREFS")
else:
    print("DEFAULT_UI_PREFS not matched, searching with regex...")
    text = re.sub(r'const DEFAULT_UI_PREFS = \{.*?\};', new_prefs, text, flags=re.DOTALL)
    print("Replaced DEFAULT_UI_PREFS via regex")

# 2. Update applyAllAppearancePrefs
old_apply_block = """  root.style.setProperty('--base-font-size', `${u.baseFontPx}px`);
  root.style.setProperty('--q-font-size', `${qRem}rem`);
  root.style.setProperty('--opt-font-size', `${optRem}rem`);"""

new_apply_block = """  root.style.setProperty('--base-font-size', `${u.baseFontPx}px`);
  root.style.setProperty('--q-font-size', `${qRem}rem`);
  root.style.setProperty('--opt-font-size', `${optRem}rem`);
  root.style.setProperty('--line-height-q', u.lineHeight || 1.62);
  root.style.setProperty('--card-radius', `${u.cardRadiusPx || 18}px`);"""

text = text.replace(old_apply_block, new_apply_block, 1)

# 3. Add slider sync inside applyAllAppearancePrefs
old_sync_sliders = """  const optSlider = document.getElementById('slider-opt-rem');
  if (optSlider) optSlider.value = optRem;
  setText('lbl-opt-rem', `${Math.round(optRem * 100)}%`);"""

new_sync_sliders = """  const optSlider = document.getElementById('slider-opt-rem');
  if (optSlider) optSlider.value = optRem;
  setText('lbl-opt-rem', `${Math.round(optRem * 100)}%`);

  const radiusSlider = document.getElementById('slider-card-radius');
  if (radiusSlider) radiusSlider.value = u.cardRadiusPx || 18;
  setText('lbl-card-radius', `${u.cardRadiusPx || 18}px`);

  const lhSlider = document.getElementById('slider-line-height');
  if (lhSlider) lhSlider.value = u.lineHeight || 1.62;
  setText('lbl-line-height', `${u.lineHeight || 1.62}x`);

  const volSlider = document.getElementById('slider-sound-vol');
  if (volSlider) volSlider.value = Math.round((u.soundVolume ?? 0.8) * 100);
  setText('lbl-sound-vol', `${Math.round((u.soundVolume ?? 0.8) * 100)}%`);

  const autoDelaySlider = document.getElementById('slider-autonext-delay');
  if (autoDelaySlider) autoDelaySlider.value = u.autoNextDelaySec || 0.8;
  setText('lbl-autonext-delay', `${u.autoNextDelaySec || 0.8}s`);

  setSelectSafe('pref-tts-speed', u.ttsSpeed || 1.0, 1.0);
  setSelectSafe('pref-shadow-depth', u.shadowDepth || 'medium', 'medium');
  setSelectSafe('pref-timer-display', u.timerMode || 'countdown', 'countdown');
  setSelectSafe('pref-anticheat-level', u.antiCheatLevel || 'medium', 'medium');
  setSelectSafe('cfg-default-tutor-persona', u.defaultTutorPersona || 'professor', 'professor');
  setSelectSafe('cfg-ai-verbosity', u.aiVerbosity || 'standard', 'standard');"""

text = text.replace(old_sync_sliders, new_sync_sliders, 1)

# 4. Update updateTypographyPrefs
old_update_fn = """function updateTypographyPrefs() {
  const fontUi = document.getElementById('pref-font-ui')?.value || DEFAULT_UI_PREFS.fontUi;
  const fontQuestion = document.getElementById('pref-font-question')?.value || 'inherit';
  const fontAnswer = document.getElementById('pref-font-answer')?.value || 'inherit';
  const fontCode = document.getElementById('pref-font-code')?.value || DEFAULT_UI_PREFS.fontCode;
  const baseFontPx = parseFloat(document.getElementById('slider-base-px')?.value || '16');
  const qFontRem = parseFloat(document.getElementById('slider-q-rem')?.value || '1.14');
  const optFontRem = parseFloat(document.getElementById('slider-opt-rem')?.value || '1.02');

  STATE.ui.fontUi = fontUi;
  STATE.ui.fontQuestion = fontQuestion;
  STATE.ui.fontAnswer = fontAnswer;
  STATE.ui.fontCode = fontCode;
  STATE.ui.baseFontPx = baseFontPx;
  STATE.ui.qFontRem = qFontRem;
  STATE.ui.optFontRem = optFontRem;

  applyAllAppearancePrefs();
  syncUserStateToServer();
}"""

new_update_fn = """function updateTypographyPrefs() {
  const fontUi = document.getElementById('pref-font-ui')?.value || DEFAULT_UI_PREFS.fontUi;
  const fontQuestion = document.getElementById('pref-font-question')?.value || 'inherit';
  const fontAnswer = document.getElementById('pref-font-answer')?.value || 'inherit';
  const fontCode = document.getElementById('pref-font-code')?.value || DEFAULT_UI_PREFS.fontCode;
  const baseFontPx = parseFloat(document.getElementById('slider-base-px')?.value || '16');
  const qFontRem = parseFloat(document.getElementById('slider-q-rem')?.value || '1.14');
  const optFontRem = parseFloat(document.getElementById('slider-opt-rem')?.value || '1.02');
  const cardRadiusPx = parseInt(document.getElementById('slider-card-radius')?.value || '18', 10);
  const lineHeight = parseFloat(document.getElementById('slider-line-height')?.value || '1.62');
  const soundVolume = parseFloat(document.getElementById('slider-sound-vol')?.value || '80') / 100;
  const autoNextDelaySec = parseFloat(document.getElementById('slider-autonext-delay')?.value || '0.8');
  const ttsSpeed = parseFloat(document.getElementById('pref-tts-speed')?.value || '1.0');
  const shadowDepth = document.getElementById('pref-shadow-depth')?.value || 'medium';
  const timerMode = document.getElementById('pref-timer-display')?.value || 'countdown';
  const antiCheatLevel = document.getElementById('pref-anticheat-level')?.value || 'medium';
  const defaultTutorPersona = document.getElementById('cfg-default-tutor-persona')?.value || 'professor';
  const aiVerbosity = document.getElementById('cfg-ai-verbosity')?.value || 'standard';

  STATE.ui.fontUi = fontUi;
  STATE.ui.fontQuestion = fontQuestion;
  STATE.ui.fontAnswer = fontAnswer;
  STATE.ui.fontCode = fontCode;
  STATE.ui.baseFontPx = baseFontPx;
  STATE.ui.qFontRem = qFontRem;
  STATE.ui.optFontRem = optFontRem;
  STATE.ui.cardRadiusPx = cardRadiusPx;
  STATE.ui.lineHeight = lineHeight;
  STATE.ui.soundVolume = soundVolume;
  STATE.ui.autoNextDelaySec = autoNextDelaySec;
  STATE.ui.ttsSpeed = ttsSpeed;
  STATE.ui.shadowDepth = shadowDepth;
  STATE.ui.timerMode = timerMode;
  STATE.ui.antiCheatLevel = antiCheatLevel;
  STATE.ui.defaultTutorPersona = defaultTutorPersona;
  STATE.ui.aiVerbosity = aiVerbosity;

  applyAllAppearancePrefs();
  syncUserStateToServer();
}"""

text = text.replace(old_update_fn, new_update_fn, 1)

# 5. Update switchSettingsTab
old_switch_tab = """function switchSettingsTab(tab) {
  ['appearance', 'sync', 'ai', 'tools'].forEach((t) => {
    document.getElementById(`stab-panel-${t}`)?.classList.toggle('hidden', t !== tab);
  });
  document.querySelectorAll('[data-stab]').forEach((btn) => {
    btn.classList.toggle('active', btn.getAttribute('data-stab') === tab);
  });
  if (tab === 'sync') fetchNetworkQrInfo();
  if (tab === 'ai') checkApiKeyStatus();
}"""

new_switch_tab = """function switchSettingsTab(tab) {
  const tabs = ['appearance', 'typography', 'ai', 'tools', 'sync'];
  tabs.forEach((t) => {
    document.getElementById(`stab-panel-${t}`)?.classList.toggle('hidden', t !== tab);
  });
  document.querySelectorAll('[data-stab]').forEach((btn) => {
    btn.classList.toggle('active', btn.getAttribute('data-stab') === tab);
  });
  if (tab === 'sync') fetchNetworkQrInfo();
  if (tab === 'ai') checkApiKeyStatus();
  if (window.lucide) { try { lucide.createIcons(); } catch (_) {} }
}"""

text = text.replace(old_switch_tab, new_switch_tab, 1)

# 6. Apply sound volume in playSound()
old_gain = "gain.gain.setValueAtTime(0.035, now);"
new_gain = "const volMul = (typeof STATE !== 'undefined' && STATE.ui && typeof STATE.ui.soundVolume === 'number') ? STATE.ui.soundVolume : 0.8;\n    gain.gain.setValueAtTime(0.035 * volMul, now);"
text = text.replace(old_gain, new_gain, 1)

# 7. Apply utter.rate in speakVietnamese()
old_utter_rate = "utter.rate = 1.04;"
new_utter_rate = "utter.rate = (typeof STATE !== 'undefined' && STATE.ui && STATE.ui.ttsSpeed) ? Number(STATE.ui.ttsSpeed) : 1.0;"
text = text.replace(old_utter_rate, new_utter_rate, 1)

with open(app_js_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated app.js with rich settings logic successfully")
