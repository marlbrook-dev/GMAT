/* @ds-bundle: {"format":4,"namespace":"GMATStudyGuideDesignSystem_efe656","components":[{"name":"Badge","sourcePath":"components/display/Badge.jsx"},{"name":"Card","sourcePath":"components/display/Card.jsx"},{"name":"Tag","sourcePath":"components/display/Tag.jsx"},{"name":"Tooltip","sourcePath":"components/display/Tooltip.jsx"},{"name":"Dialog","sourcePath":"components/feedback/Dialog.jsx"},{"name":"ProgressBar","sourcePath":"components/feedback/ProgressBar.jsx"},{"name":"Toast","sourcePath":"components/feedback/Toast.jsx"},{"name":"Button","sourcePath":"components/forms/Button.jsx"},{"name":"Checkbox","sourcePath":"components/forms/Checkbox.jsx"},{"name":"IconButton","sourcePath":"components/forms/IconButton.jsx"},{"name":"Input","sourcePath":"components/forms/Input.jsx"},{"name":"Radio","sourcePath":"components/forms/Radio.jsx"},{"name":"Select","sourcePath":"components/forms/Select.jsx"},{"name":"Switch","sourcePath":"components/forms/Switch.jsx"},{"name":"Dropdown","sourcePath":"components/navigation/Dropdown.jsx"},{"name":"Tabs","sourcePath":"components/navigation/Tabs.jsx"},{"name":"Flashcard","sourcePath":"components/study/Flashcard.jsx"},{"name":"QuizOption","sourcePath":"components/study/QuizOption.jsx"},{"name":"StatTile","sourcePath":"components/study/StatTile.jsx"}],"sourceHashes":{"components/display/Badge.jsx":"8777e787a525","components/display/Card.jsx":"8e27b622d657","components/display/Tag.jsx":"55495ca335e8","components/display/Tooltip.jsx":"dede4e474760","components/feedback/Dialog.jsx":"9fb4c22e1c04","components/feedback/ProgressBar.jsx":"f870733a87f0","components/feedback/Toast.jsx":"a89a8bd0605c","components/forms/Button.jsx":"fb5bf994eb85","components/forms/Checkbox.jsx":"713793dd8bb2","components/forms/IconButton.jsx":"f53d7cd3ac10","components/forms/Input.jsx":"da15ea9f5a36","components/forms/Radio.jsx":"02dc64676362","components/forms/Select.jsx":"d413a9f1864e","components/forms/Switch.jsx":"27724b3e4550","components/navigation/Dropdown.jsx":"8dfe36fb479a","components/navigation/Tabs.jsx":"fb39f71d9908","components/study/Flashcard.jsx":"1335e9da2c4c","components/study/QuizOption.jsx":"608fdbf7e11b","components/study/StatTile.jsx":"ef98576c37aa","ui_kits/web_app/Account.jsx":"37255335748c","ui_kits/web_app/Admin.jsx":"4592d04d9f26","ui_kits/web_app/AppShell.jsx":"7afe19662d8f","ui_kits/web_app/Dashboard.jsx":"716cf1aff2f2","ui_kits/web_app/Onboarding.jsx":"a711d510e4b6","ui_kits/web_app/Practice.jsx":"4ad3bc77a123","ui_kits/web_app/Results.jsx":"040b904189f5"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.GMATStudyGuideDesignSystem_efe656 = window.GMATStudyGuideDesignSystem_efe656 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/display/Badge.jsx
try { (() => {
const T = {
  success: ['var(--status-success-bg)', 'var(--green-700)', 'var(--green-100)'],
  error: ['var(--status-error-bg)', 'var(--status-error)', 'var(--red-100)'],
  warning: ['var(--status-warning-bg)', 'var(--status-warning)', 'var(--amber-100)'],
  info: ['var(--status-info-bg)', 'var(--status-info)', 'var(--blue-100)'],
  neutral: ['var(--gray-100)', 'var(--gray-700)', 'var(--gray-200)'],
  accent: ['var(--brand-accent-soft)', 'var(--gold-700)', 'var(--gold-100)']
};
function Badge({
  tone = 'neutral',
  children,
  style
}) {
  const [bg, fg, bd] = T[tone] || T.neutral;
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 6,
      background: bg,
      color: fg,
      border: '1px solid ' + bd,
      borderRadius: 'var(--radius-pill)',
      padding: '2px 10px',
      fontFamily: 'var(--font-body)',
      fontSize: 12,
      fontWeight: 600,
      lineHeight: 1.6,
      ...style
    }
  }, children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/Badge.jsx", error: String((e && e.message) || e) }); }

// components/display/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Card({
  title,
  action,
  children,
  padding = 'var(--space-6)',
  hoverable = false,
  style,
  ...rest
}) {
  const [h, setH] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", _extends({
    onMouseEnter: () => setH(true),
    onMouseLeave: () => setH(false),
    style: {
      background: 'var(--surface-card)',
      border: '1px solid var(--border-default)',
      borderRadius: 'var(--radius-lg)',
      boxShadow: hoverable && h ? 'var(--shadow-md)' : 'var(--shadow-sm)',
      padding,
      transition: 'box-shadow var(--duration-base) var(--ease-out)',
      fontFamily: 'var(--font-body)',
      ...style
    }
  }, rest), (title || action) && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      marginBottom: 'var(--space-4)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-display)',
      fontWeight: 700,
      fontSize: 17,
      color: 'var(--text-heading)'
    }
  }, title), action), children);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/Card.jsx", error: String((e && e.message) || e) }); }

// components/display/Tag.jsx
try { (() => {
function Tag({
  children,
  onRemove,
  style
}) {
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 6,
      background: 'var(--surface-sunken)',
      color: 'var(--text-body)',
      borderRadius: 'var(--radius-sm)',
      padding: '3px 8px',
      fontFamily: 'var(--font-body)',
      fontSize: 13,
      fontWeight: 500,
      ...style
    }
  }, children, onRemove && /*#__PURE__*/React.createElement("button", {
    onClick: onRemove,
    "aria-label": "Remove",
    style: {
      border: 'none',
      background: 'none',
      cursor: 'pointer',
      padding: 0,
      display: 'inline-flex',
      color: 'var(--text-muted)'
    }
  }, /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    width: "12",
    height: "12",
    style: {
      stroke: 'currentColor',
      fill: 'none',
      strokeWidth: 2.5,
      strokeLinecap: 'round'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "M18 6 6 18M6 6l12 12"
  }))));
}
Object.assign(__ds_scope, { Tag });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/Tag.jsx", error: String((e && e.message) || e) }); }

// components/display/Tooltip.jsx
try { (() => {
function Tooltip({
  text,
  children
}) {
  const [show, setShow] = React.useState(false);
  return /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'relative',
      display: 'inline-flex'
    },
    onMouseEnter: () => setShow(true),
    onMouseLeave: () => setShow(false)
  }, children, show && /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      bottom: 'calc(100% + 8px)',
      left: '50%',
      transform: 'translateX(-50%)',
      background: 'var(--surface-inverse)',
      color: '#fff',
      fontFamily: 'var(--font-body)',
      fontSize: 12,
      fontWeight: 500,
      lineHeight: 1.4,
      padding: '6px 10px',
      borderRadius: 'var(--radius-sm)',
      whiteSpace: 'nowrap',
      boxShadow: 'var(--shadow-lg)',
      zIndex: 10
    }
  }, text));
}
Object.assign(__ds_scope, { Tooltip });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/Tooltip.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Dialog.jsx
try { (() => {
function Dialog({
  open,
  title,
  children,
  footer,
  onClose,
  width = 440
}) {
  if (!open) return null;
  return /*#__PURE__*/React.createElement("div", {
    onClick: onClose,
    style: {
      position: 'fixed',
      inset: 0,
      background: 'rgba(11,18,32,.45)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 'var(--z-modal)',
      padding: 24
    }
  }, /*#__PURE__*/React.createElement("div", {
    onClick: e => e.stopPropagation(),
    style: {
      background: 'var(--surface-card)',
      borderRadius: 'var(--radius-lg)',
      boxShadow: 'var(--shadow-lg)',
      width,
      maxWidth: '100%',
      padding: 'var(--space-6)',
      fontFamily: 'var(--font-body)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-display)',
      fontWeight: 800,
      fontSize: 20,
      color: 'var(--text-heading)',
      marginBottom: 'var(--space-3)'
    }
  }, title), /*#__PURE__*/React.createElement("div", {
    style: {
      color: 'var(--text-body)',
      fontSize: 15
    }
  }, children), footer && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'flex-end',
      gap: 'var(--space-3)',
      marginTop: 'var(--space-6)'
    }
  }, footer)));
}
Object.assign(__ds_scope, { Dialog });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Dialog.jsx", error: String((e && e.message) || e) }); }

// components/feedback/ProgressBar.jsx
try { (() => {
function ProgressBar({
  value = 0,
  max = 100,
  color = 'var(--brand-primary)',
  height = 8,
  label,
  style
}) {
  const pct = Math.max(0, Math.min(100, value / max * 100));
  return /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-body)',
      ...style
    }
  }, label && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      fontSize: 12,
      fontWeight: 600,
      color: 'var(--text-muted)',
      marginBottom: 6
    }
  }, /*#__PURE__*/React.createElement("span", null, label), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)'
    }
  }, Math.round(pct), "%")), /*#__PURE__*/React.createElement("div", {
    style: {
      height,
      background: 'var(--surface-sunken)',
      borderRadius: 'var(--radius-pill)',
      overflow: 'hidden'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: pct + '%',
      height: '100%',
      background: color,
      borderRadius: 'var(--radius-pill)',
      transition: 'width var(--duration-base) var(--ease-out)'
    }
  })));
}
Object.assign(__ds_scope, { ProgressBar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/ProgressBar.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Toast.jsx
try { (() => {
const T = {
  success: ['var(--status-success)', 'var(--status-success-bg)', 'var(--green-100)'],
  error: ['var(--status-error)', 'var(--status-error-bg)', 'var(--red-100)'],
  info: ['var(--status-info)', 'var(--status-info-bg)', 'var(--blue-100)'],
  warning: ['var(--status-warning)', 'var(--status-warning-bg)', 'var(--amber-100)']
};
function Toast({
  tone = 'info',
  children,
  onDismiss,
  style
}) {
  const [fg, bg, bd] = T[tone] || T.info;
  return /*#__PURE__*/React.createElement("div", {
    role: "status",
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      background: bg,
      border: '1px solid ' + bd,
      borderLeft: 'none',
      borderRadius: 'var(--radius-md)',
      padding: '10px 14px',
      fontFamily: 'var(--font-body)',
      fontSize: 14,
      color: 'var(--text-heading)',
      boxShadow: 'var(--shadow-md)',
      ...style
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 8,
      height: 8,
      borderRadius: '50%',
      background: fg,
      flexShrink: 0
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1
    }
  }, children), onDismiss && /*#__PURE__*/React.createElement("button", {
    onClick: onDismiss,
    "aria-label": "Dismiss",
    style: {
      border: 'none',
      background: 'none',
      cursor: 'pointer',
      padding: 0,
      color: 'var(--text-muted)',
      display: 'inline-flex'
    }
  }, /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    width: "14",
    height: "14",
    style: {
      stroke: 'currentColor',
      fill: 'none',
      strokeWidth: 2.5,
      strokeLinecap: 'round'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "M18 6 6 18M6 6l12 12"
  }))));
}
Object.assign(__ds_scope, { Toast });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Toast.jsx", error: String((e && e.message) || e) }); }

// components/forms/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const V = {
  primary: {
    background: 'var(--brand-primary)',
    color: '#fff',
    border: '1px solid transparent'
  },
  secondary: {
    background: 'var(--surface-card)',
    color: 'var(--text-heading)',
    border: '1px solid var(--border-strong)'
  },
  ghost: {
    background: 'transparent',
    color: 'var(--brand-primary)',
    border: '1px solid transparent'
  },
  danger: {
    background: 'var(--status-error)',
    color: '#fff',
    border: '1px solid transparent'
  }
};
const S = {
  sm: {
    fontSize: 13,
    padding: '6px 12px'
  },
  md: {
    fontSize: 15,
    padding: '9px 18px'
  },
  lg: {
    fontSize: 17,
    padding: '12px 24px'
  }
};
function Button({
  variant = 'primary',
  size = 'md',
  disabled,
  children,
  style,
  ...rest
}) {
  const [st, setSt] = React.useState('idle');
  const [fv, setFv] = React.useState(false);
  const base = {
    fontFamily: 'var(--font-display)',
    fontWeight: 700,
    borderRadius: 'var(--radius-md)',
    cursor: disabled ? 'default' : 'pointer',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    lineHeight: 1.2,
    transition: 'background var(--duration-fast) var(--ease-out),transform var(--duration-fast) var(--ease-out)',
    opacity: disabled ? 0.5 : 1,
    outline: 'none',
    boxShadow: fv ? 'var(--focus-ring)' : 'none',
    ...V[variant],
    ...S[size]
  };
  if (!disabled && st !== 'idle') {
    if (variant === 'primary') base.background = 'var(--brand-primary-hover)';
    if (variant === 'secondary') base.background = 'var(--gray-50)';
    if (variant === 'ghost') base.background = 'var(--brand-primary-soft)';
    if (variant === 'danger') base.background = '#B91C1C';
    if (st === 'press') base.transform = 'scale(.97)';
  }
  return /*#__PURE__*/React.createElement("button", _extends({
    disabled: disabled,
    onMouseEnter: () => setSt('hover'),
    onMouseLeave: () => setSt('idle'),
    onMouseDown: () => setSt('press'),
    onMouseUp: () => setSt('hover'),
    onFocus: e => setFv(e.target.matches(':focus-visible')),
    onBlur: () => setFv(false),
    style: {
      ...base,
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Button.jsx", error: String((e && e.message) || e) }); }

// components/forms/Checkbox.jsx
try { (() => {
function Checkbox({
  label,
  checked,
  defaultChecked = false,
  onChange,
  disabled
}) {
  const [on, setOn] = React.useState(defaultChecked);
  const c = checked !== undefined ? checked : on;
  const toggle = () => {
    if (disabled) return;
    setOn(!c);
    onChange && onChange(!c);
  };
  return /*#__PURE__*/React.createElement("label", {
    onClick: toggle,
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 10,
      cursor: disabled ? 'default' : 'pointer',
      opacity: disabled ? 0.5 : 1,
      fontFamily: 'var(--font-body)',
      fontSize: 15,
      color: 'var(--text-heading)',
      userSelect: 'none'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 18,
      height: 18,
      borderRadius: 'var(--radius-sm)',
      border: '1.5px solid ' + (c ? 'var(--brand-primary)' : 'var(--border-strong)'),
      background: c ? 'var(--brand-primary)' : 'var(--surface-card)',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      transition: 'background var(--duration-fast) var(--ease-out)'
    }
  }, c && /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    width: "12",
    height: "12",
    style: {
      stroke: '#fff',
      fill: 'none',
      strokeWidth: 3.5,
      strokeLinecap: 'round',
      strokeLinejoin: 'round'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "m5 13 4 4L19 7"
  }))), label);
}
Object.assign(__ds_scope, { Checkbox });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Checkbox.jsx", error: String((e && e.message) || e) }); }

// components/forms/IconButton.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function IconButton({
  variant = 'subtle',
  size = 'md',
  label,
  disabled,
  children,
  style,
  ...rest
}) {
  const [h, setH] = React.useState(false);
  const [fv, setFv] = React.useState(false);
  const px = {
    sm: 28,
    md: 36,
    lg: 44
  }[size];
  const base = {
    width: px,
    height: px,
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 'var(--radius-md)',
    cursor: disabled ? 'default' : 'pointer',
    color: 'var(--text-body)',
    transition: 'background var(--duration-fast) var(--ease-out)',
    opacity: disabled ? 0.5 : 1,
    outline: 'none',
    boxShadow: fv ? 'var(--focus-ring)' : 'none',
    background: variant === 'outline' ? 'var(--surface-card)' : 'transparent',
    border: variant === 'outline' ? '1px solid var(--border-strong)' : '1px solid transparent'
  };
  if (h && !disabled) base.background = variant === 'outline' ? 'var(--gray-50)' : 'var(--gray-100)';
  return /*#__PURE__*/React.createElement("button", _extends({
    "aria-label": label,
    title: label,
    disabled: disabled,
    onMouseEnter: () => setH(true),
    onMouseLeave: () => setH(false),
    onFocus: e => setFv(e.target.matches(':focus-visible')),
    onBlur: () => setFv(false),
    style: {
      ...base,
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { IconButton });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/IconButton.jsx", error: String((e && e.message) || e) }); }

// components/forms/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Input({
  label,
  hint,
  error,
  style,
  inputStyle,
  ...rest
}) {
  const [f, setF] = React.useState(false);
  return /*#__PURE__*/React.createElement("label", {
    style: {
      display: 'grid',
      gap: 6,
      fontFamily: 'var(--font-body)',
      ...style
    }
  }, label && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 13,
      fontWeight: 600,
      color: 'var(--text-heading)'
    }
  }, label), /*#__PURE__*/React.createElement("input", _extends({
    onFocus: () => setF(true),
    onBlur: () => setF(false),
    style: {
      font: 'inherit',
      fontSize: 15,
      color: 'var(--text-heading)',
      background: 'var(--surface-card)',
      border: '1px solid ' + (error ? 'var(--status-error)' : f ? 'var(--brand-primary)' : 'var(--border-strong)'),
      borderRadius: 'var(--radius-md)',
      padding: '9px 12px',
      outline: 'none',
      boxShadow: f ? 'var(--focus-ring)' : 'none',
      transition: 'box-shadow var(--duration-fast) var(--ease-out)',
      ...inputStyle
    }
  }, rest)), error ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 12,
      color: 'var(--status-error)'
    }
  }, error) : hint ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 12,
      color: 'var(--text-muted)'
    }
  }, hint) : null);
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Input.jsx", error: String((e && e.message) || e) }); }

// components/forms/Radio.jsx
try { (() => {
function Radio({
  label,
  checked,
  onChange,
  disabled,
  name,
  value
}) {
  return /*#__PURE__*/React.createElement("label", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 10,
      cursor: disabled ? 'default' : 'pointer',
      opacity: disabled ? 0.5 : 1,
      fontFamily: 'var(--font-body)',
      fontSize: 15,
      color: 'var(--text-heading)',
      userSelect: 'none'
    },
    onClick: () => !disabled && onChange && onChange(value)
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 18,
      height: 18,
      borderRadius: '50%',
      border: '1.5px solid ' + (checked ? 'var(--brand-primary)' : 'var(--border-strong)'),
      background: 'var(--surface-card)',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center'
    }
  }, checked && /*#__PURE__*/React.createElement("span", {
    style: {
      width: 10,
      height: 10,
      borderRadius: '50%',
      background: 'var(--brand-primary)'
    }
  })), label);
}
Object.assign(__ds_scope, { Radio });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Radio.jsx", error: String((e && e.message) || e) }); }

// components/forms/Select.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function Select({
  label,
  options = [],
  style,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("label", {
    style: {
      display: 'grid',
      gap: 6,
      fontFamily: 'var(--font-body)',
      ...style
    }
  }, label && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 13,
      fontWeight: 600,
      color: 'var(--text-heading)'
    }
  }, label), /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'relative',
      display: 'block'
    }
  }, /*#__PURE__*/React.createElement("select", _extends({
    style: {
      font: 'inherit',
      fontSize: 15,
      color: 'var(--text-heading)',
      background: 'var(--surface-card)',
      border: '1px solid var(--border-strong)',
      borderRadius: 'var(--radius-md)',
      padding: '9px 34px 9px 12px',
      width: '100%',
      appearance: 'none',
      outline: 'none'
    }
  }, rest), options.map(o => /*#__PURE__*/React.createElement("option", {
    key: o.value ?? o,
    value: o.value ?? o
  }, o.label ?? o))), /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    width: "16",
    height: "16",
    style: {
      position: 'absolute',
      right: 10,
      top: '50%',
      transform: 'translateY(-50%)',
      pointerEvents: 'none',
      stroke: 'var(--text-muted)',
      fill: 'none',
      strokeWidth: 2,
      strokeLinecap: 'round',
      strokeLinejoin: 'round'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "m6 9 6 6 6-6"
  }))));
}
Object.assign(__ds_scope, { Select });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Select.jsx", error: String((e && e.message) || e) }); }

// components/forms/Switch.jsx
try { (() => {
function Switch({
  label,
  checked,
  defaultChecked = false,
  onChange,
  disabled
}) {
  const [on, setOn] = React.useState(defaultChecked);
  const c = checked !== undefined ? checked : on;
  const toggle = () => {
    if (disabled) return;
    setOn(!c);
    onChange && onChange(!c);
  };
  return /*#__PURE__*/React.createElement("label", {
    onClick: toggle,
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 10,
      cursor: disabled ? 'default' : 'pointer',
      opacity: disabled ? 0.5 : 1,
      fontFamily: 'var(--font-body)',
      fontSize: 15,
      color: 'var(--text-heading)',
      userSelect: 'none'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 36,
      height: 20,
      borderRadius: 'var(--radius-pill)',
      background: c ? 'var(--brand-primary)' : 'var(--gray-300)',
      position: 'relative',
      transition: 'background var(--duration-base) var(--ease-out)',
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      top: 2,
      left: c ? 18 : 2,
      width: 16,
      height: 16,
      borderRadius: '50%',
      background: '#fff',
      boxShadow: 'var(--shadow-sm)',
      transition: 'left var(--duration-base) var(--ease-out)'
    }
  })), label);
}
Object.assign(__ds_scope, { Switch });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Switch.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Dropdown.jsx
try { (() => {
function Dropdown({
  label,
  items = [],
  onSelect,
  align = 'left'
}) {
  const [open, setOpen] = React.useState(false);
  const [fv, setFv] = React.useState(false);
  const ref = React.useRef(null);
  React.useEffect(() => {
    if (!open) return;
    const onDoc = e => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    };
    const onKey = e => {
      if (e.key === 'Escape') setOpen(false);
    };
    document.addEventListener('mousedown', onDoc);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', onDoc);
      document.removeEventListener('keydown', onKey);
    };
  }, [open]);
  return /*#__PURE__*/React.createElement("div", {
    ref: ref,
    style: {
      position: 'relative',
      display: 'inline-block',
      isolation: 'isolate'
    }
  }, /*#__PURE__*/React.createElement("button", {
    "aria-haspopup": "menu",
    "aria-expanded": open,
    onClick: () => setOpen(!open),
    onFocus: e => setFv(e.target.matches(':focus-visible')),
    onBlur: () => setFv(false),
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 7,
      fontFamily: 'var(--font-display)',
      fontWeight: 700,
      fontSize: 14,
      color: 'var(--text-heading)',
      background: 'var(--surface-card)',
      border: '1px solid var(--border-strong)',
      borderRadius: 'var(--radius-md)',
      padding: '8px 14px',
      cursor: 'pointer',
      outline: 'none',
      boxShadow: fv ? 'var(--focus-ring)' : 'none'
    }
  }, label, /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    width: "14",
    height: "14",
    style: {
      stroke: 'var(--text-muted)',
      fill: 'none',
      strokeWidth: 2,
      strokeLinecap: 'round',
      strokeLinejoin: 'round',
      transform: open ? 'rotate(180deg)' : 'none',
      transition: 'transform var(--duration-fast) var(--ease-out)'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "m6 9 6 6 6-6"
  }))), open && /*#__PURE__*/React.createElement("div", {
    role: "menu",
    style: {
      position: 'absolute',
      top: 'calc(100% + 8px)',
      [align === 'right' ? 'right' : 'left']: 0,
      minWidth: 200,
      background: 'var(--surface-card)',
      border: '1px solid var(--border-default)',
      borderRadius: 'var(--radius-lg)',
      boxShadow: 'var(--shadow-lg)',
      padding: 6,
      display: 'grid',
      zIndex: 'var(--z-dropdown)'
    }
  }, items.map(it => {
    const v = it.value ?? it,
      l = it.label ?? it;
    return /*#__PURE__*/React.createElement("button", {
      key: v,
      role: "menuitem",
      onClick: () => {
        setOpen(false);
        onSelect && onSelect(v);
      },
      style: {
        textAlign: 'left',
        border: 'none',
        background: 'transparent',
        cursor: 'pointer',
        padding: '9px 12px',
        borderRadius: 'var(--radius-md)',
        fontFamily: 'var(--font-display)',
        fontWeight: 600,
        fontSize: 14,
        color: 'var(--text-heading)'
      },
      onMouseEnter: e => {
        e.currentTarget.style.background = 'var(--brand-primary-soft)';
        e.currentTarget.style.color = 'var(--brand-primary)';
      },
      onMouseLeave: e => {
        e.currentTarget.style.background = 'transparent';
        e.currentTarget.style.color = 'var(--text-heading)';
      }
    }, l);
  })));
}
Object.assign(__ds_scope, { Dropdown });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Dropdown.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Tabs.jsx
try { (() => {
function Tabs({
  items = [],
  active,
  defaultActive,
  onChange,
  style
}) {
  const [cur, setCur] = React.useState(defaultActive ?? items[0]);
  const a = active !== undefined ? active : cur;
  return /*#__PURE__*/React.createElement("div", {
    role: "tablist",
    style: {
      display: 'flex',
      gap: 'var(--space-6)',
      borderBottom: '1px solid var(--border-default)',
      fontFamily: 'var(--font-display)',
      ...style
    }
  }, items.map(t => /*#__PURE__*/React.createElement("button", {
    key: t,
    role: "tab",
    "aria-selected": t === a,
    onClick: () => {
      setCur(t);
      onChange && onChange(t);
    },
    onFocus: e => {
      if (e.target.matches(':focus-visible')) e.target.style.boxShadow = 'var(--focus-ring)';
    },
    onBlur: e => {
      e.target.style.boxShadow = 'none';
    },
    style: {
      borderRadius: 'var(--radius-sm)',
      border: 'none',
      background: 'none',
      cursor: 'pointer',
      padding: '10px 2px',
      fontFamily: 'inherit',
      fontSize: 15,
      fontWeight: 700,
      color: t === a ? 'var(--brand-primary)' : 'var(--text-muted)',
      borderBottom: '2px solid ' + (t === a ? 'var(--brand-primary)' : 'transparent'),
      marginBottom: -1,
      outline: 'none',
      transition: 'box-shadow var(--duration-fast) var(--ease-out),' + 'color var(--duration-fast) var(--ease-out)'
    }
  }, t)));
}
Object.assign(__ds_scope, { Tabs });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Tabs.jsx", error: String((e && e.message) || e) }); }

// components/study/Flashcard.jsx
try { (() => {
function Flashcard({
  front,
  back,
  frontLabel = 'TERM',
  backLabel = 'DEFINITION',
  width = '100%',
  height = 200,
  style
}) {
  const [flip, setFlip] = React.useState(false);
  const face = {
    position: 'absolute',
    inset: 0,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 12,
    borderRadius: 'var(--radius-lg)',
    padding: '24px 28px',
    backfaceVisibility: 'hidden',
    WebkitBackfaceVisibility: 'hidden',
    textAlign: 'center',
    boxSizing: 'border-box'
  };
  return /*#__PURE__*/React.createElement("button", {
    onClick: () => setFlip(!flip),
    "aria-pressed": flip,
    style: {
      display: 'block',
      width,
      height,
      perspective: '1000px',
      border: 'none',
      background: 'none',
      padding: 0,
      cursor: 'pointer',
      ...style
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'relative',
      display: 'block',
      width: '100%',
      height: '100%',
      transformStyle: 'preserve-3d',
      transform: flip ? 'rotateX(180deg)' : 'none',
      transition: 'transform 320ms var(--ease-out)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      ...face,
      background: 'var(--surface-card)',
      border: '1px solid var(--border-default)',
      boxShadow: 'var(--shadow-md)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 10,
      fontWeight: 600,
      letterSpacing: 'var(--tracking-caps)',
      color: 'var(--text-muted)'
    }
  }, frontLabel), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-serif-display)',
      fontWeight: 700,
      fontSize: 22,
      color: 'var(--text-heading)',
      lineHeight: 1.3
    }
  }, front), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 12,
      color: 'var(--text-muted)'
    }
  }, "Click to flip")), /*#__PURE__*/React.createElement("span", {
    style: {
      ...face,
      background: 'var(--navy-900)',
      border: '1px solid var(--navy-900)',
      boxShadow: 'var(--shadow-md)',
      transform: 'rotateX(180deg)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 10,
      fontWeight: 600,
      letterSpacing: 'var(--tracking-caps)',
      color: 'var(--gold-500)'
    }
  }, backLabel), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: 16,
      color: '#fff',
      lineHeight: 1.5
    }
  }, back))));
}
Object.assign(__ds_scope, { Flashcard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/study/Flashcard.jsx", error: String((e && e.message) || e) }); }

// components/study/QuizOption.jsx
try { (() => {
function QuizOption({
  letter,
  children,
  state = 'idle',
  onClick,
  style
}) {
  const [h, setH] = React.useState(false);
  const [fv, setFv] = React.useState(false);
  const map = {
    idle: {
      bd: 'var(--border-default)',
      bg: 'var(--surface-card)',
      chipBg: 'var(--surface-sunken)',
      chipFg: 'var(--text-body)'
    },
    selected: {
      bd: 'var(--brand-primary)',
      bg: 'var(--brand-primary-soft)',
      chipBg: 'var(--brand-primary)',
      chipFg: '#fff'
    },
    correct: {
      bd: 'var(--status-success)',
      bg: 'var(--status-success-bg)',
      chipBg: 'var(--status-success)',
      chipFg: '#fff'
    },
    incorrect: {
      bd: 'var(--status-error)',
      bg: 'var(--status-error-bg)',
      chipBg: 'var(--status-error)',
      chipFg: '#fff'
    }
  };
  const s = map[state] || map.idle;
  return /*#__PURE__*/React.createElement("button", {
    onClick: onClick,
    onMouseEnter: () => setH(true),
    onMouseLeave: () => setH(false),
    onFocus: e => setFv(e.target.matches(':focus-visible')),
    onBlur: () => setFv(false),
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 12,
      width: '100%',
      textAlign: 'left',
      background: state === 'idle' && h ? 'var(--gray-50)' : s.bg,
      border: '1.5px solid ' + (state === 'idle' && h ? 'var(--border-strong)' : s.bd),
      borderRadius: 'var(--radius-md)',
      padding: '12px 14px',
      cursor: 'pointer',
      fontFamily: 'var(--font-body)',
      fontSize: 15,
      color: 'var(--text-heading)',
      outline: 'none',
      boxShadow: fv ? 'var(--focus-ring)' : 'none',
      transition: 'background var(--duration-fast) var(--ease-out),border-color var(--duration-fast) var(--ease-out),box-shadow var(--duration-fast) var(--ease-out)',
      ...style
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 26,
      height: 26,
      borderRadius: 'var(--radius-sm)',
      background: s.chipBg,
      color: s.chipFg,
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'var(--font-display)',
      fontWeight: 700,
      fontSize: 13,
      flexShrink: 0
    }
  }, letter), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1
    }
  }, children), state === 'correct' && /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    width: "18",
    height: "18",
    style: {
      stroke: 'var(--status-success)',
      fill: 'none',
      strokeWidth: 3,
      strokeLinecap: 'round',
      strokeLinejoin: 'round'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "m5 13 4 4L19 7"
  })), state === 'incorrect' && /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    width: "18",
    height: "18",
    style: {
      stroke: 'var(--status-error)',
      fill: 'none',
      strokeWidth: 3,
      strokeLinecap: 'round'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "M18 6 6 18M6 6l12 12"
  })));
}
Object.assign(__ds_scope, { QuizOption });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/study/QuizOption.jsx", error: String((e && e.message) || e) }); }

// components/study/StatTile.jsx
try { (() => {
function StatTile({
  label,
  value,
  delta,
  deltaTone = 'success',
  style
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      background: 'var(--surface-card)',
      border: '1px solid var(--border-default)',
      borderRadius: 'var(--radius-lg)',
      boxShadow: 'var(--shadow-sm)',
      padding: 'var(--space-5)',
      fontFamily: 'var(--font-body)',
      ...style
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12,
      fontWeight: 600,
      letterSpacing: 'var(--tracking-caps)',
      textTransform: 'uppercase',
      color: 'var(--text-muted)'
    }
  }, label), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'baseline',
      gap: 10,
      marginTop: 6
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 30,
      fontWeight: 500,
      color: 'var(--text-heading)',
      fontVariantNumeric: 'tabular-nums'
    }
  }, value), delta && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 13,
      fontWeight: 600,
      color: deltaTone === 'success' ? 'var(--status-success)' : deltaTone === 'error' ? 'var(--status-error)' : 'var(--text-muted)'
    }
  }, delta)));
}
Object.assign(__ds_scope, { StatTile });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/study/StatTile.jsx", error: String((e && e.message) || e) }); }

// ui_kits/web_app/Account.jsx
try { (() => {
const NSacct = window.GMATStudyGuideDesignSystem_efe656;
function Account({
  onNewProgram
}) {
  const {
    Card,
    Button,
    Badge,
    Switch,
    Input
  } = NSacct;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 'var(--container-narrow)',
      margin: '0 auto',
      display: 'grid',
      gap: 'var(--space-4)'
    }
  }, /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 'var(--text-2xl)',
      fontWeight: 800
    }
  }, "Account"), /*#__PURE__*/React.createElement(Card, {
    title: "Profile"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: 14
    }
  }, /*#__PURE__*/React.createElement(Input, {
    label: "First name",
    defaultValue: "Jordan"
  }), /*#__PURE__*/React.createElement(Input, {
    label: "Last name",
    defaultValue: "Wells"
  }), /*#__PURE__*/React.createElement(Input, {
    label: "Email",
    defaultValue: "jordan@school.edu",
    hint: "Used to sign in and sync progress",
    style: {
      gridColumn: '1 / -1'
    }
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'flex-end',
      marginTop: 16
    }
  }, /*#__PURE__*/React.createElement(Button, {
    size: "sm",
    variant: "secondary"
  }, "Save changes"))), /*#__PURE__*/React.createElement(Card, {
    title: "Study program",
    action: /*#__PURE__*/React.createElement(Badge, {
      tone: "info"
    }, "Active")
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gap: 8,
      fontSize: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--text-muted)'
    }
  }, "Exam"), /*#__PURE__*/React.createElement("strong", {
    style: {
      color: 'var(--text-heading)'
    }
  }, "GMAT")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--text-muted)'
    }
  }, "Goal"), /*#__PURE__*/React.createElement("strong", {
    style: {
      color: 'var(--text-heading)'
    }
  }, "Score 675+ for M7 programs")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--text-muted)'
    }
  }, "Time budget"), /*#__PURE__*/React.createElement("strong", {
    style: {
      color: 'var(--text-heading)'
    }
  }, "3\u20135 hrs / week"))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 10,
      justifyContent: 'flex-end',
      marginTop: 16
    }
  }, /*#__PURE__*/React.createElement(Button, {
    size: "sm",
    variant: "ghost",
    onClick: onNewProgram
  }, "Start another exam"), /*#__PURE__*/React.createElement(Button, {
    size: "sm",
    variant: "secondary"
  }, "Edit program"))), /*#__PURE__*/React.createElement(Card, {
    title: "Plan & billing",
    action: /*#__PURE__*/React.createElement(Badge, {
      tone: "accent"
    }, "Quarterly")
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gap: 8,
      fontSize: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--text-muted)'
    }
  }, "Price"), /*#__PURE__*/React.createElement("strong", {
    style: {
      color: 'var(--text-heading)',
      fontFamily: 'var(--font-mono)'
    }
  }, "$44.99 / 3 months")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--text-muted)'
    }
  }, "Renews"), /*#__PURE__*/React.createElement("strong", {
    style: {
      color: 'var(--text-heading)'
    }
  }, "November 17, 2026"))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 10,
      justifyContent: 'flex-end',
      marginTop: 16
    }
  }, /*#__PURE__*/React.createElement(Button, {
    size: "sm",
    variant: "ghost"
  }, "Cancel plan"), /*#__PURE__*/React.createElement(Button, {
    size: "sm",
    variant: "secondary"
  }, "Change plan"))), /*#__PURE__*/React.createElement(Card, {
    title: "Notifications"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gap: 14
    }
  }, /*#__PURE__*/React.createElement(Switch, {
    label: "Daily study reminder",
    defaultChecked: true
  }), /*#__PURE__*/React.createElement(Switch, {
    label: "Weekly progress digest",
    defaultChecked: true
  }), /*#__PURE__*/React.createElement(Switch, {
    label: "Product news"
  }))), /*#__PURE__*/React.createElement(Card, {
    title: "Privacy & data"
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontSize: 14,
      color: 'var(--text-body)'
    }
  }, "We store your answers, pace, and scores to power your adaptive plan. You can take a copy anytime or delete everything for good."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 10,
      justifyContent: 'flex-end',
      marginTop: 16
    }
  }, /*#__PURE__*/React.createElement(Button, {
    size: "sm",
    variant: "secondary"
  }, "Download my data"), /*#__PURE__*/React.createElement(Button, {
    size: "sm",
    variant: "danger"
  }, "Delete account"))));
}
Object.assign(window, {
  Account
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/web_app/Account.jsx", error: String((e && e.message) || e) }); }

// ui_kits/web_app/Admin.jsx
try { (() => {
const NSadm = window.GMATStudyGuideDesignSystem_efe656;
const EVENTS = [['3:42 pm', 'u_18h2', 'round_completed', '{exam:"GMAT", mode:"quick10", correct:8, secs:641}'], ['3:41 pm', 'u_2c91', 'question_answered', '{qid:"ds_114", correct:false, secs:118}'], ['3:39 pm', 'u_9ak2', 'plan_selected', '{plan:"quarterly", trial:false}'], ['3:38 pm', 'u_9ak2', 'account_created', '{exam:"LSAT", source:"organic"}'], ['3:35 pm', 'u_77fe', 'round_started', '{exam:"GRE", mode:"flashcards"}'], ['3:31 pm', 'u_18h2', 'wizard_completed', '{exam:"GMAT", hours:"3-5", tools:3}']];
function Admin() {
  const {
    Card,
    Button,
    Badge,
    Switch,
    Input,
    StatTile,
    Tabs
  } = NSadm;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gap: 'var(--space-6)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 12,
      background: 'var(--brand-accent-soft)',
      border: '1px solid var(--gold-100)',
      borderRadius: 'var(--radius-md)',
      padding: '10px 14px'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 8,
      height: 8,
      borderRadius: '50%',
      background: 'var(--gold-600)'
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-display)',
      fontWeight: 700,
      fontSize: 13,
      color: 'var(--gold-700)'
    }
  }, "Owner view \u2014 users never see this. Changes publish instantly.")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'flex-end',
      justifyContent: 'space-between'
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 'var(--text-2xl)',
      fontWeight: 800
    }
  }, "Command center"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: '6px 0 0',
      color: 'var(--text-muted)'
    }
  }, "Last 7 days \xB7 all exams")), /*#__PURE__*/React.createElement(Button, {
    variant: "secondary"
  }, "Export CSV")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: 'repeat(4,1fr)',
      gap: 'var(--space-4)'
    }
  }, /*#__PURE__*/React.createElement(StatTile, {
    label: "Signups",
    value: "1,284",
    delta: "+12%"
  }), /*#__PURE__*/React.createElement(StatTile, {
    label: "Daily active",
    value: "4,102",
    delta: "+5%"
  }), /*#__PURE__*/React.createElement(StatTile, {
    label: "Round completion",
    value: "87%",
    delta: "+1%"
  }), /*#__PURE__*/React.createElement(StatTile, {
    label: "Free \u2192 paid",
    value: "6.4%",
    delta: "\u22120.3%",
    deltaTone: "error"
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1.5fr 1fr',
      gap: 'var(--space-4)',
      alignItems: 'start'
    }
  }, /*#__PURE__*/React.createElement(Card, {
    title: "Live events",
    action: /*#__PURE__*/React.createElement(Badge, {
      tone: "success"
    }, "Streaming")
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gap: 6
    }
  }, EVENTS.map(([t, u, ev, props], i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 12,
      padding: '8px 10px',
      background: 'var(--surface-sunken)',
      borderRadius: 'var(--radius-sm)',
      fontFamily: 'var(--font-mono)',
      fontSize: 12
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--text-muted)',
      width: 56,
      flexShrink: 0
    }
  }, t), /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--text-muted)',
      width: 52,
      flexShrink: 0
    }
  }, u), /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--navy-800)',
      fontWeight: 500,
      width: 130,
      flexShrink: 0
    }
  }, ev), /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--text-muted)',
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      whiteSpace: 'nowrap'
    }
  }, props)))), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 12,
      color: 'var(--text-muted)',
      margin: '12px 0 0'
    }
  }, "Full schema in guidelines/data-analytics.md \u2014 every event, its properties, and retention rules.")), /*#__PURE__*/React.createElement(Card, {
    title: "Site settings"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gap: 14
    }
  }, /*#__PURE__*/React.createElement(Switch, {
    label: "Guarantee banner",
    defaultChecked: true
  }), /*#__PURE__*/React.createElement(Switch, {
    label: "New-user wizard",
    defaultChecked: true
  }), /*#__PURE__*/React.createElement(Switch, {
    label: "Promo pricing"
  }), /*#__PURE__*/React.createElement(Input, {
    label: "Banner text",
    defaultValue: "Built for the current GMAT (Focus Edition) \xB7 70-point improvement guarantee"
  }), /*#__PURE__*/React.createElement(Input, {
    label: "Monthly price (USD)",
    defaultValue: "19.99"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'flex-end'
    }
  }, /*#__PURE__*/React.createElement(Button, {
    size: "sm"
  }, "Publish"))))), /*#__PURE__*/React.createElement(Card, {
    title: "Question bank",
    action: /*#__PURE__*/React.createElement(Button, {
      size: "sm",
      variant: "secondary"
    }, "Add question")
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gap: 6
    }
  }, [['ds_114', 'Is n even? (1) 3n is even…', 'Data Insights', 'Data Sufficiency', '62% correct'], ['al_078', 'If 3x − 7 = 2x + 5…', 'Quantitative', 'Algebra', '81% correct'], ['cr_201', 'The columnist argues that…', 'Verbal', 'Critical Reasoning', '54% correct']].map(([id, q, section, tag, rate]) => /*#__PURE__*/React.createElement("div", {
    key: id,
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 12,
      padding: '10px 12px',
      background: 'var(--surface-sunken)',
      borderRadius: 'var(--radius-md)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 12,
      color: 'var(--text-muted)',
      width: 52,
      flexShrink: 0
    }
  }, id), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      fontSize: 14,
      color: 'var(--text-heading)',
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      whiteSpace: 'nowrap'
    }
  }, q), /*#__PURE__*/React.createElement(Badge, {
    tone: section === 'Quantitative' ? 'info' : section === 'Verbal' ? 'accent' : 'neutral'
  }, tag), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 12,
      color: 'var(--text-muted)',
      flexShrink: 0
    }
  }, rate), /*#__PURE__*/React.createElement(Button, {
    size: "sm",
    variant: "ghost"
  }, "Edit"))))));
}
Object.assign(window, {
  Admin
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/web_app/Admin.jsx", error: String((e && e.message) || e) }); }

// ui_kits/web_app/AppShell.jsx
try { (() => {
function AppShell({
  active,
  onNav,
  children,
  view = 'user',
  onToggleView,
  onAccount
}) {
  const {
    Badge
  } = window.GMATStudyGuideDesignSystem_efe656;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      minHeight: '100vh',
      background: 'var(--surface-page)'
    }
  }, /*#__PURE__*/React.createElement("header", {
    style: {
      background: 'var(--surface-card)',
      borderBottom: '1px solid var(--border-default)',
      position: 'sticky',
      top: 0,
      zIndex: 20
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 'var(--container-max)',
      margin: '0 auto',
      padding: '0 var(--space-6)',
      height: 60,
      display: 'flex',
      alignItems: 'center',
      gap: 32
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 9,
      whiteSpace: 'nowrap'
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/logo.svg",
    width: "30",
    height: "30",
    alt: ""
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-serif-display)',
      fontWeight: 700,
      fontSize: 19,
      color: 'var(--navy-900)'
    }
  }, "Start From ", /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--gold-600)'
    }
  }, "Nowhere"))), /*#__PURE__*/React.createElement("nav", {
    style: {
      display: 'flex',
      gap: 4,
      flex: 1
    }
  }, ['Dashboard', 'Practice', 'Review'].map(t => /*#__PURE__*/React.createElement("button", {
    key: t,
    onClick: () => onNav(t),
    style: {
      border: 'none',
      cursor: 'pointer',
      fontFamily: 'var(--font-display)',
      fontWeight: 700,
      fontSize: 14,
      padding: '7px 14px',
      borderRadius: 'var(--radius-md)',
      background: active === t ? 'var(--brand-primary-soft)' : 'transparent',
      color: active === t ? 'var(--brand-primary)' : 'var(--text-muted)'
    }
  }, t))), /*#__PURE__*/React.createElement(Badge, {
    tone: "accent"
  }, "Streak \xD77"), /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      border: '1px solid var(--border-strong)',
      borderRadius: 'var(--radius-pill)',
      padding: 2,
      gap: 2
    },
    title: "Prototype only: switch between user and owner views"
  }, ['User', 'Owner'].map(v => /*#__PURE__*/React.createElement("button", {
    key: v,
    onClick: () => onToggleView && onToggleView(v.toLowerCase()),
    "aria-pressed": view === v.toLowerCase(),
    style: {
      border: 'none',
      cursor: 'pointer',
      fontFamily: 'var(--font-display)',
      fontWeight: 700,
      fontSize: 11,
      padding: '4px 10px',
      borderRadius: 999,
      background: view === v.toLowerCase() ? 'var(--navy-800)' : 'transparent',
      color: view === v.toLowerCase() ? '#fff' : 'var(--text-muted)'
    }
  }, v))), /*#__PURE__*/React.createElement("button", {
    onClick: () => onAccount && onAccount(),
    "aria-label": "Account",
    style: {
      width: 34,
      height: 34,
      borderRadius: '50%',
      background: 'var(--navy-100)',
      color: 'var(--navy-800)',
      border: 'none',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'var(--font-display)',
      fontWeight: 800,
      fontSize: 13
    }
  }, "JW"))), /*#__PURE__*/React.createElement("main", {
    style: {
      maxWidth: 'var(--container-max)',
      margin: '0 auto',
      padding: 'var(--space-8) var(--space-6)'
    }
  }, children));
}
Object.assign(window, {
  AppShell
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/web_app/AppShell.jsx", error: String((e && e.message) || e) }); }

// ui_kits/web_app/Dashboard.jsx
try { (() => {
function Dashboard({
  onStart,
  onNewProgram
}) {
  const {
    Card,
    Button,
    Badge,
    ProgressBar,
    StatTile,
    Tabs
  } = window.GMATStudyGuideDesignSystem_efe656;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gap: 'var(--space-6)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'flex-end',
      justifyContent: 'space-between',
      gap: 16
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 'var(--text-2xl)',
      fontWeight: 800
    }
  }, "Good morning, Jordan"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: '6px 0 0',
      color: 'var(--text-muted)'
    }
  }, "Test day is in 34 days. You're on pace.")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 12
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    size: "lg",
    onClick: onNewProgram
  }, "New program"), /*#__PURE__*/React.createElement(Button, {
    size: "lg",
    onClick: onStart
  }, "Start today's round"))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: 'repeat(4,1fr)',
      gap: 'var(--space-4)'
    }
  }, /*#__PURE__*/React.createElement(StatTile, {
    label: "Est. score",
    value: "645",
    delta: "+15"
  }), /*#__PURE__*/React.createElement(StatTile, {
    label: "Accuracy",
    value: "78%",
    delta: "+2%"
  }), /*#__PURE__*/React.createElement(StatTile, {
    label: "Questions today",
    value: "14",
    delta: "of 30",
    deltaTone: "neutral"
  }), /*#__PURE__*/React.createElement(StatTile, {
    label: "Avg. pace",
    value: "1:52",
    delta: "\u22120:08"
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1.4fr 1fr',
      gap: 'var(--space-4)',
      alignItems: 'start'
    }
  }, /*#__PURE__*/React.createElement(Card, {
    title: "Section mastery",
    action: /*#__PURE__*/React.createElement(Badge, {
      tone: "info"
    }, "Adaptive")
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gap: 'var(--space-4)'
    }
  }, /*#__PURE__*/React.createElement(ProgressBar, {
    label: "Quantitative",
    value: 62,
    color: "var(--section-quant)"
  }), /*#__PURE__*/React.createElement(ProgressBar, {
    label: "Verbal",
    value: 71,
    color: "var(--section-verbal)"
  }), /*#__PURE__*/React.createElement(ProgressBar, {
    label: "Data Insights",
    value: 44,
    color: "var(--section-data)"
  })), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: '16px 0 0',
      fontSize: 13,
      color: 'var(--text-muted)'
    }
  }, "Data Insights is your weakest area \u2014 today's round leans into table analysis.")), /*#__PURE__*/React.createElement(Card, {
    title: "Today's plan",
    action: /*#__PURE__*/React.createElement(Badge, {
      tone: "accent"
    }, "Day 12")
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gap: 10
    }
  }, [['Quick 10 · Quant', '~12 min', true], ['Timed sprint · Data Insights', '~10 min', false], ['Flashcards · Idioms', '~5 min', false]].map(([t, d, done]) => /*#__PURE__*/React.createElement("div", {
    key: t,
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      padding: '10px 12px',
      background: 'var(--surface-sunken)',
      borderRadius: 'var(--radius-md)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 18,
      height: 18,
      borderRadius: '50%',
      flexShrink: 0,
      border: done ? 'none' : '1.5px solid var(--border-strong)',
      background: done ? 'var(--status-success)' : 'transparent',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center'
    }
  }, done && /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    width: "11",
    height: "11",
    style: {
      stroke: '#fff',
      fill: 'none',
      strokeWidth: 3.5,
      strokeLinecap: 'round',
      strokeLinejoin: 'round'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "m5 13 4 4L19 7"
  }))), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      fontSize: 14,
      fontWeight: 500,
      color: done ? 'var(--text-muted)' : 'var(--text-heading)',
      textDecoration: done ? 'line-through' : 'none'
    }
  }, t), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 12,
      color: 'var(--text-muted)'
    }
  }, d)))))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h2", {
    style: {
      fontSize: 'var(--text-lg)',
      fontWeight: 800,
      marginBottom: 'var(--space-4)'
    }
  }, "Games"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: 'repeat(4,1fr)',
      gap: 'var(--space-4)'
    }
  }, [['Quick 10', 'Ten adaptive questions, no timer.', 'var(--section-quant)', 'var(--section-quant-bg)'], ['Timed sprint', 'Beat the clock — 2 min per question.', 'var(--section-data)', 'var(--section-data-bg)'], ['Flashcards', 'Flip through formulas and idioms.', 'var(--section-verbal)', 'var(--section-verbal-bg)'], ['Mock section', 'Full 45-minute section, exam rules.', 'var(--gray-700)', 'var(--gray-100)']].map(([t, d, fg, bg]) => /*#__PURE__*/React.createElement(Card, {
    key: t,
    hoverable: true,
    padding: "var(--space-5)",
    onClick: onStart,
    style: {
      cursor: 'pointer'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-block',
      width: 34,
      height: 34,
      borderRadius: 'var(--radius-md)',
      background: bg,
      marginBottom: 12,
      position: 'relative'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      inset: 11,
      borderRadius: 3,
      background: fg
    }
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-display)',
      fontWeight: 700,
      fontSize: 15,
      color: 'var(--text-heading)'
    }
  }, t), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13,
      color: 'var(--text-muted)',
      marginTop: 4
    }
  }, d))))));
}
Object.assign(window, {
  Dashboard
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/web_app/Dashboard.jsx", error: String((e && e.message) || e) }); }

// ui_kits/web_app/Onboarding.jsx
try { (() => {
const EXAM_DATA = {
  'GMAT': {
    color: 'var(--section-quant)',
    goals: ['Score 675+ for M7 programs', 'Fix my Quant from the diagnostic', 'Balance all three sections', 'Retake — beat my 615'],
    tools: [['Quick 10', 'Adaptive daily rounds — the core loop', true], ['Timed sprint', 'Pace training for Data Insights', true], ['Flashcards', 'Idioms and formula recall', false], ['Mock section', 'Full 45-minute exam-rules section', false]]
  },
  'GRE': {
    color: 'var(--section-verbal)',
    goals: ['Score 325+ for PhD programs', 'Grow my Verbal vocab fast', 'Quant refresh after years out'],
    tools: [['Quick 10', 'Adaptive daily rounds', true], ['Flashcards', 'Vocabulary decks — the GRE staple', true], ['Timed sprint', 'Pace training', false], ['Essay outliner', 'AWA structure drills', false]]
  },
  'LSAT': {
    color: 'var(--section-data)',
    goals: ['Score 170+ for T14 schools', 'Master Logic Games', 'Speed up Reading Comp'],
    tools: [['Logic drills', 'Argument-pattern rounds', true], ['Timed sprint', 'Section pacing', true], ['Flashcards', 'Flaw types and conditionals', false], ['Mock section', 'Full timed section', false]]
  },
  'MCAT': {
    color: 'var(--status-error)',
    goals: ['Score 515+ for MD programs', 'CARS is my weak spot', 'Content review before practice'],
    tools: [['Quick 10', 'Adaptive daily rounds', true], ['Flashcards', 'High-yield content recall', true], ['CARS passages', 'Daily timed passage', true], ['Mock section', 'Full-length section', false]]
  },
  'Executive Assessment': {
    color: 'var(--gold-600)',
    goals: ['Hit 155+ for EMBA', 'Study around a full-time job'],
    tools: [['Quick 10', 'Adaptive daily rounds', true], ['Timed sprint', 'IR pacing', true], ['Flashcards', 'Formula recall', false]]
  }
};
function FloatCard({
  style,
  children
}) {
  return /*#__PURE__*/React.createElement("div", {
    "aria-hidden": "true",
    style: {
      position: 'absolute',
      background: 'var(--surface-card)',
      border: '1px solid var(--border-default)',
      borderRadius: 'var(--radius-lg)',
      boxShadow: 'var(--shadow-lg)',
      padding: 16,
      opacity: .55,
      pointerEvents: 'none',
      ...style
    }
  }, children);
}
function Onboarding({
  open,
  onClose,
  onComplete
}) {
  const NS = window.GMATStudyGuideDesignSystem_efe656;
  const {
    Button
  } = NS;
  const [step, setStep] = React.useState(0);
  const [exam, setExam] = React.useState(null);
  const [goal, setGoal] = React.useState('');
  const [hours, setHours] = React.useState('3–5 hrs / week');
  const [tools, setTools] = React.useState({});
  const [first, setFirst] = React.useState('');
  const [last, setLast] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [consent, setConsent] = React.useState(false);
  const [plan, setPlan] = React.useState('Quarterly');
  React.useEffect(() => {
    if (exam) {
      const t = {};
      EXAM_DATA[exam].tools.forEach(([n,, on]) => t[n] = on);
      setTools(t);
    }
  }, [exam]);
  React.useEffect(() => {
    const onKey = e => {
      if (e.key === 'Escape') onClose();
    };
    if (open) {
      document.addEventListener('keydown', onKey);
      return () => document.removeEventListener('keydown', onKey);
    }
  }, [open]);
  if (!open) return null;
  const d = exam ? EXAM_DATA[exam] : null;
  const suggestions = d ? d.goals.filter(g => !goal || g.toLowerCase().includes(goal.toLowerCase()) || goal.length < 3).slice(0, 4) : [];
  const total = 6;
  const acctOk = first.trim().length > 0 && email.includes('@') && consent;
  const canNext = [true, !!exam, goal.trim().length > 0, true, true, acctOk, true][step];
  const finish = () => onComplete({
    exam: exam || 'GMAT',
    goal: goal || (d ? d.goals[0] : ''),
    hours,
    tools,
    account: {
      first,
      last,
      email,
      consent
    },
    plan
  });
  const chip = active => ({
    fontFamily: 'var(--font-display)',
    fontWeight: 600,
    fontSize: 14,
    color: active ? '#fff' : 'var(--text-heading)',
    background: active ? 'var(--brand-primary)' : 'var(--surface-card)',
    border: '1px solid ' + (active ? 'var(--brand-primary)' : 'var(--border-strong)'),
    borderRadius: 999,
    padding: '9px 18px',
    cursor: 'pointer',
    transition: 'background var(--duration-fast) var(--ease-out),border-color var(--duration-fast) var(--ease-out)'
  });
  const sugLabel = /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 7
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/logo.svg",
    width: "16",
    height: "16",
    alt: ""
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-display)',
      fontWeight: 700,
      fontSize: 13,
      color: 'var(--text-heading)'
    }
  }, "Suggestions"));
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'fixed',
      inset: 0,
      background: 'var(--navy-50)',
      zIndex: 'var(--z-modal)',
      overflow: 'auto',
      isolation: 'isolate'
    }
  }, /*#__PURE__*/React.createElement(FloatCard, {
    style: {
      top: '14%',
      left: '4%',
      width: 150,
      transform: 'rotate(-5deg)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 22,
      color: 'var(--navy-800)'
    }
  }, "645"), /*#__PURE__*/React.createElement("div", {
    style: {
      height: 6,
      background: 'var(--surface-sunken)',
      borderRadius: 999,
      marginTop: 8
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: '62%',
      height: '100%',
      background: 'var(--gold-500)',
      borderRadius: 999
    }
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      height: 6,
      background: 'var(--surface-sunken)',
      borderRadius: 999,
      marginTop: 6
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: '40%',
      height: '100%',
      background: 'var(--section-quant)',
      borderRadius: 999
    }
  }))), /*#__PURE__*/React.createElement(FloatCard, {
    style: {
      bottom: '12%',
      left: '9%',
      width: 170,
      transform: 'rotate(4deg)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-serif-display)',
      fontWeight: 700,
      fontSize: 14,
      color: 'var(--navy-900)'
    }
  }, "Weighted average"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11,
      color: 'var(--text-muted)',
      marginTop: 6
    }
  }, "The mean leans toward the larger group\u2026")), /*#__PURE__*/React.createElement(FloatCard, {
    style: {
      top: '18%',
      right: '5%',
      width: 160,
      transform: 'rotate(5deg)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 8,
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 22,
      height: 22,
      borderRadius: 6,
      background: 'var(--brand-primary)',
      color: '#fff',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'var(--font-display)',
      fontWeight: 700,
      fontSize: 11
    }
  }, "B"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 12,
      color: 'var(--text-heading)'
    }
  }, "x = 12")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 8,
      alignItems: 'center',
      marginTop: 8
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 22,
      height: 22,
      borderRadius: 6,
      background: 'var(--surface-sunken)',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'var(--font-display)',
      fontWeight: 700,
      fontSize: 11,
      color: 'var(--text-body)'
    }
  }, "C"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 12,
      color: 'var(--text-muted)'
    }
  }, "x = 14"))), /*#__PURE__*/React.createElement(FloatCard, {
    style: {
      bottom: '16%',
      right: '8%',
      width: 150,
      transform: 'rotate(-4deg)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 18,
      color: 'var(--navy-800)'
    }
  }, "01:47"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11,
      color: 'var(--text-muted)',
      marginTop: 4
    }
  }, "12 / 20 correct")), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '22px 36px'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 9
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/logo.svg",
    width: "26",
    height: "26",
    alt: ""
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-serif-display)',
      fontWeight: 700,
      fontSize: 18,
      color: 'var(--navy-900)'
    }
  }, "Start From ", /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--gold-600)'
    }
  }, "Nowhere"))), /*#__PURE__*/React.createElement("button", {
    onClick: onClose,
    style: {
      border: 'none',
      background: 'none',
      cursor: 'pointer',
      fontFamily: 'var(--font-display)',
      fontWeight: 700,
      fontSize: 14,
      color: 'var(--text-heading)'
    }
  }, "Skip to dashboard \u2192")), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      maxWidth: 760,
      margin: '4vh auto 40px',
      padding: '0 24px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    role: "dialog",
    "aria-modal": "true",
    "aria-label": "Start a new study program",
    style: {
      background: 'var(--surface-card)',
      borderRadius: 'var(--radius-lg)',
      boxShadow: 'var(--shadow-lg)',
      padding: '0 0 28px',
      overflow: 'hidden'
    }
  }, step > 0 && /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '28px 56px 0'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: 3,
      background: 'var(--gray-200)',
      borderRadius: 999
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: '100%',
      width: step / total * 100 + '%',
      background: 'var(--brand-primary)',
      borderRadius: 999,
      transition: 'width var(--duration-base) var(--ease-out)'
    }
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '40px 56px 8px',
      textAlign: 'center',
      minHeight: 330
    }
  }, step === 0 && /*#__PURE__*/React.createElement("div", {
    style: {
      paddingTop: 24
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/logo.svg",
    width: "48",
    height: "48",
    alt: ""
  }), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 36,
      marginTop: 20,
      textWrap: 'pretty'
    }
  }, "Let's build your study program"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 16,
      color: 'var(--text-muted)',
      maxWidth: 440,
      margin: '14px auto 0'
    }
  }, "Answer a few questions in your own words and get a plan that fits your exam, your goal, and your schedule."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 18,
      justifyContent: 'center',
      alignItems: 'center',
      marginTop: 32
    }
  }, /*#__PURE__*/React.createElement(Button, {
    size: "lg",
    onClick: () => setStep(1)
  }, "Let's go"), /*#__PURE__*/React.createElement("button", {
    onClick: finish,
    style: {
      border: 'none',
      background: 'none',
      cursor: 'pointer',
      fontFamily: 'var(--font-display)',
      fontWeight: 700,
      fontSize: 15,
      color: 'var(--text-heading)',
      textDecoration: 'underline'
    }
  }, "Skip the questions"))), step === 1 && /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 34,
      marginTop: 24
    }
  }, "First, which exam is it?"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 14,
      color: 'var(--text-muted)',
      margin: '10px 0 0'
    }
  }, "Sections, games, and the score model all adjust to your exam."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 10,
      justifyContent: 'center',
      flexWrap: 'wrap',
      marginTop: 28,
      maxWidth: 520,
      marginLeft: 'auto',
      marginRight: 'auto'
    }
  }, Object.keys(EXAM_DATA).map(name => /*#__PURE__*/React.createElement("button", {
    key: name,
    onClick: () => setExam(name),
    "aria-pressed": exam === name,
    style: chip(exam === name)
  }, name)))), step === 2 && /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 34,
      marginTop: 24
    }
  }, "What are your goals?"), /*#__PURE__*/React.createElement("input", {
    autoFocus: true,
    value: goal,
    onChange: e => setGoal(e.target.value),
    placeholder: 'Enter or select your goal',
    style: {
      width: '100%',
      maxWidth: 560,
      boxSizing: 'border-box',
      font: 'inherit',
      fontSize: 16,
      color: 'var(--text-heading)',
      border: '1.5px solid var(--border-strong)',
      borderRadius: 'var(--radius-md)',
      padding: '14px 18px',
      marginTop: 28,
      outline: 'none',
      textAlign: 'left'
    },
    onFocus: e => {
      e.target.style.borderColor = 'var(--brand-primary)';
      e.target.style.boxShadow = 'var(--focus-ring)';
    },
    onBlur: e => {
      e.target.style.borderColor = 'var(--border-strong)';
      e.target.style.boxShadow = 'none';
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 560,
      margin: '20px auto 0',
      textAlign: 'left'
    }
  }, sugLabel, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 8,
      flexWrap: 'wrap',
      marginTop: 12
    }
  }, suggestions.map(s => /*#__PURE__*/React.createElement("button", {
    key: s,
    onClick: () => setGoal(s),
    style: {
      fontFamily: 'var(--font-display)',
      fontWeight: 600,
      fontSize: 13,
      color: 'var(--text-heading)',
      background: 'var(--surface-card)',
      border: '1px solid var(--border-strong)',
      borderRadius: 999,
      padding: '7px 14px',
      cursor: 'pointer'
    }
  }, s))), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 12,
      color: 'var(--text-muted)',
      marginTop: 14
    }
  }, "Suggestions come from goals of ", exam, " students with similar diagnostics."))), step === 3 && /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 34,
      marginTop: 24
    }
  }, "How much time can you give it?"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 14,
      color: 'var(--text-muted)',
      margin: '10px 0 0'
    }
  }, "Honest beats ambitious \u2014 the plan rebuilds itself if life gets in the way."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 10,
      justifyContent: 'center',
      flexWrap: 'wrap',
      marginTop: 28
    }
  }, ['Under 3 hrs / week', '3–5 hrs / week', '6–10 hrs / week', '10+ hrs / week'].map(h => /*#__PURE__*/React.createElement("button", {
    key: h,
    onClick: () => setHours(h),
    "aria-pressed": hours === h,
    style: chip(hours === h)
  }, h)))), step === 4 && /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 34,
      marginTop: 24,
      textWrap: 'pretty'
    }
  }, "Add tools to reach your goal"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 14,
      color: 'var(--text-muted)',
      margin: '10px 0 0'
    }
  }, "You can add or remove them later."), /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 560,
      margin: '22px auto 0',
      textAlign: 'left'
    }
  }, d.tools.map(([name, why]) => /*#__PURE__*/React.createElement("button", {
    key: name,
    onClick: () => setTools({
      ...tools,
      [name]: !tools[name]
    }),
    "aria-pressed": !!tools[name],
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 14,
      width: '100%',
      textAlign: 'left',
      padding: '15px 4px',
      background: 'none',
      border: 'none',
      borderBottom: '1px solid var(--border-default)',
      cursor: 'pointer'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 19,
      height: 19,
      borderRadius: 'var(--radius-sm)',
      flexShrink: 0,
      border: tools[name] ? 'none' : '1.5px solid var(--border-strong)',
      background: tools[name] ? 'var(--brand-primary)' : 'transparent',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      transition: 'background var(--duration-fast) var(--ease-out)'
    }
  }, tools[name] && /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    width: "12",
    height: "12",
    style: {
      stroke: '#fff',
      fill: 'none',
      strokeWidth: 3.5,
      strokeLinecap: 'round',
      strokeLinejoin: 'round'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "m5 13 4 4L19 7"
  }))), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 15,
      color: 'var(--text-body)'
    }
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      fontFamily: 'var(--font-display)',
      fontWeight: 700,
      color: 'var(--text-heading)'
    }
  }, name), " \u2014 ", why))))), step === 5 && /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 34,
      marginTop: 24
    }
  }, "Create your account"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 14,
      color: 'var(--text-muted)',
      margin: '10px 0 0'
    }
  }, "Basic info for your account and study personalization."), /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 400,
      margin: '24px auto 0',
      display: 'grid',
      gap: 14,
      textAlign: 'left'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: 12
    }
  }, /*#__PURE__*/React.createElement("label", {
    style: {
      display: 'grid',
      gap: 6
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 13,
      fontWeight: 600,
      color: 'var(--text-heading)'
    }
  }, "First name"), /*#__PURE__*/React.createElement("input", {
    value: first,
    onChange: e => setFirst(e.target.value),
    style: {
      font: 'inherit',
      fontSize: 15,
      color: 'var(--text-heading)',
      border: '1.5px solid var(--border-strong)',
      borderRadius: 'var(--radius-md)',
      padding: '10px 12px',
      outline: 'none'
    }
  })), /*#__PURE__*/React.createElement("label", {
    style: {
      display: 'grid',
      gap: 6
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 13,
      fontWeight: 600,
      color: 'var(--text-heading)'
    }
  }, "Last name"), /*#__PURE__*/React.createElement("input", {
    value: last,
    onChange: e => setLast(e.target.value),
    style: {
      font: 'inherit',
      fontSize: 15,
      color: 'var(--text-heading)',
      border: '1.5px solid var(--border-strong)',
      borderRadius: 'var(--radius-md)',
      padding: '10px 12px',
      outline: 'none'
    }
  }))), /*#__PURE__*/React.createElement("label", {
    style: {
      display: 'grid',
      gap: 6
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 13,
      fontWeight: 600,
      color: 'var(--text-heading)'
    }
  }, "Email"), /*#__PURE__*/React.createElement("input", {
    type: "email",
    value: email,
    onChange: e => setEmail(e.target.value),
    placeholder: "you@school.edu",
    style: {
      font: 'inherit',
      fontSize: 15,
      color: 'var(--text-heading)',
      border: '1.5px solid var(--border-strong)',
      borderRadius: 'var(--radius-md)',
      padding: '10px 12px',
      outline: 'none'
    }
  })), /*#__PURE__*/React.createElement("label", {
    style: {
      display: 'flex',
      alignItems: 'flex-start',
      gap: 10,
      cursor: 'pointer',
      fontSize: 13,
      color: 'var(--text-body)'
    },
    onClick: () => setConsent(!consent)
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 18,
      height: 18,
      marginTop: 1,
      borderRadius: 'var(--radius-sm)',
      flexShrink: 0,
      border: consent ? 'none' : '1.5px solid var(--border-strong)',
      background: consent ? 'var(--brand-primary)' : 'transparent',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center'
    }
  }, consent && /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    width: "11",
    height: "11",
    style: {
      stroke: '#fff',
      fill: 'none',
      strokeWidth: 3.5,
      strokeLinecap: 'round',
      strokeLinejoin: 'round'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "m5 13 4 4L19 7"
  }))), /*#__PURE__*/React.createElement("span", null, "I agree to the ", /*#__PURE__*/React.createElement("a", {
    href: "../website/terms.html",
    target: "_blank",
    onClick: e => e.stopPropagation()
  }, "Terms of Use"), " and ", /*#__PURE__*/React.createElement("a", {
    href: "#",
    onClick: e => {
      e.preventDefault();
      e.stopPropagation();
    }
  }, "Privacy Policy"))), /*#__PURE__*/React.createElement("p", {
    style: {
      display: 'flex',
      gap: 8,
      fontSize: 12,
      color: 'var(--text-muted)',
      margin: '4px 0 0'
    }
  }, /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    width: "14",
    height: "14",
    style: {
      stroke: 'var(--gold-600)',
      fill: 'none',
      strokeWidth: 2,
      strokeLinecap: 'round',
      strokeLinejoin: 'round',
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("rect", {
    x: "5",
    y: "11",
    width: "14",
    height: "10",
    rx: "2"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M8 11V7a4 4 0 0 1 8 0v4"
  })), /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: 'var(--text-heading)'
    }
  }, "Your data is safe with us."), " Email creates your account and syncs progress across devices.")))), step === 6 && /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 34,
      marginTop: 24
    }
  }, "Choose your plan"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 14,
      color: 'var(--text-muted)',
      margin: '10px 0 0'
    }
  }, "Study when and how you want. Cancel anytime."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr 1fr',
      gap: 14,
      maxWidth: 600,
      margin: '26px auto 0'
    }
  }, [['Monthly', '$19.99', '$19.99/mo · billed monthly', null], ['Quarterly', '$44.99', '$15.00/mo · billed every 3 months', 'Save 25%'], ['Annual', '$119.99', '$10.00/mo · billed annually', 'Save 50%']].map(([name, price, detail, save]) => /*#__PURE__*/React.createElement("button", {
    key: name,
    onClick: () => setPlan(name),
    "aria-pressed": plan === name,
    style: {
      position: 'relative',
      textAlign: 'center',
      padding: '22px 14px 18px',
      borderRadius: 'var(--radius-lg)',
      cursor: 'pointer',
      background: plan === name ? 'var(--brand-primary-soft)' : 'var(--surface-card)',
      border: '1.5px solid ' + (plan === name ? 'var(--brand-primary)' : 'var(--border-default)'),
      transition: 'border-color var(--duration-fast) var(--ease-out)'
    }
  }, save && /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      top: -10,
      left: '50%',
      transform: 'translateX(-50%)',
      fontFamily: 'var(--font-display)',
      fontWeight: 700,
      fontSize: 11,
      color: 'var(--navy-900)',
      background: 'var(--gold-500)',
      borderRadius: 999,
      padding: '2px 10px',
      whiteSpace: 'nowrap'
    }
  }, save), /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'block',
      fontFamily: 'var(--font-display)',
      fontWeight: 700,
      fontSize: 15,
      color: 'var(--text-heading)'
    }
  }, name), /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'block',
      fontFamily: 'var(--font-mono)',
      fontSize: 24,
      color: 'var(--navy-800)',
      marginTop: 6
    }
  }, price), /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'block',
      fontSize: 11,
      color: 'var(--text-muted)',
      marginTop: 6
    }
  }, detail)))), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 13,
      marginTop: 20
    }
  }, /*#__PURE__*/React.createElement("a", {
    href: "#",
    onClick: e => e.preventDefault()
  }, "Or try your first 20 questions free"), " \u2014 no card required."))), step > 0 && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '18px 56px 0'
    }
  }, /*#__PURE__*/React.createElement("button", {
    onClick: () => setStep(step - 1),
    style: {
      border: 'none',
      background: 'none',
      cursor: 'pointer',
      fontFamily: 'var(--font-display)',
      fontWeight: 700,
      fontSize: 15,
      color: 'var(--text-heading)',
      display: 'inline-flex',
      alignItems: 'center',
      gap: 6
    }
  }, /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    width: "14",
    height: "14",
    style: {
      stroke: 'currentColor',
      fill: 'none',
      strokeWidth: 2.5,
      strokeLinecap: 'round',
      strokeLinejoin: 'round'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "m15 18-6-6 6-6"
  })), "Back"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 22
    }
  }, step < 6 && step !== 5 && /*#__PURE__*/React.createElement("button", {
    onClick: () => setStep(step + 1),
    style: {
      border: 'none',
      background: 'none',
      cursor: 'pointer',
      fontFamily: 'var(--font-display)',
      fontWeight: 700,
      fontSize: 15,
      color: 'var(--text-muted)'
    }
  }, "Skip"), step < 6 ? /*#__PURE__*/React.createElement(Button, {
    disabled: !canNext,
    onClick: () => setStep(step + 1)
  }, "Continue") : /*#__PURE__*/React.createElement(Button, {
    onClick: finish
  }, "Start studying")))), /*#__PURE__*/React.createElement("p", {
    style: {
      textAlign: 'center',
      fontSize: 12,
      color: 'var(--text-muted)',
      marginTop: 18
    }
  }, "Assist can make mistakes \u2014 your plan stays fully editable.")));
}
Object.assign(window, {
  Onboarding,
  EXAM_DATA
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/web_app/Onboarding.jsx", error: String((e && e.message) || e) }); }

// ui_kits/web_app/Practice.jsx
try { (() => {
const BANK = [{
  section: 'Quantitative',
  tag: 'Algebra',
  q: 'If 3x − 7 = 2x + 5, what is the value of x?',
  opts: ['x = 8', 'x = 10', 'x = 12', 'x = 14'],
  correct: 2,
  explain: 'Subtract 2x from both sides: x − 7 = 5, so x = 12.'
}, {
  section: 'Quantitative',
  tag: 'Arithmetic',
  q: 'A store marks up an item 25% and then discounts it 20%. The final price is what percent of the original?',
  opts: ['95%', '100%', '102.5%', '105%'],
  correct: 1,
  explain: '1.25 × 0.80 = 1.00 — exactly the original price.'
}, {
  section: 'Data Insights',
  tag: 'Data Sufficiency',
  q: 'Is n even? (1) 3n is even. (2) n + 2 is even.',
  opts: ['Statement 1 alone is sufficient', 'Statement 2 alone is sufficient', 'Each alone is sufficient', 'Both together are needed'],
  correct: 2,
  explain: 'If 3n is even, n is even. If n + 2 is even, n is even. Each works alone.'
}];
function Practice({
  onFinish,
  onExit
}) {
  const {
    Card,
    Button,
    Badge,
    ProgressBar,
    QuizOption
  } = window.GMATStudyGuideDesignSystem_efe656;
  const [i, setI] = React.useState(0);
  const [sel, setSel] = React.useState(null);
  const [revealed, setRevealed] = React.useState(false);
  const [score, setScore] = React.useState(0);
  const q = BANK[i];
  const next = () => {
    if (i + 1 >= BANK.length) {
      onFinish(score + (revealed && sel === q.correct ? 0 : 0));
    } else {
      setI(i + 1);
      setSel(null);
      setRevealed(false);
    }
  };
  const submit = () => {
    setRevealed(true);
    if (sel === q.correct) setScore(score + 1);
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 'var(--container-narrow)',
      margin: '0 auto',
      display: 'grid',
      gap: 'var(--space-4)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 16
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: q.section === 'Quantitative' ? 'success' : 'info'
  }, q.section), /*#__PURE__*/React.createElement(Badge, {
    tone: "neutral"
  }, q.tag), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement(ProgressBar, {
    value: i + (revealed ? 1 : 0),
    max: BANK.length,
    height: 6
  })), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 14,
      color: 'var(--text-muted)'
    }
  }, i + 1, " / ", BANK.length), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 14,
      fontWeight: 500,
      color: 'var(--text-heading)',
      background: 'var(--surface-sunken)',
      padding: '4px 10px',
      borderRadius: 'var(--radius-sm)'
    }
  }, "01:47")), /*#__PURE__*/React.createElement(Card, {
    padding: "var(--space-8)"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-display)',
      fontWeight: 700,
      fontSize: 'var(--text-lg)',
      color: 'var(--text-heading)',
      lineHeight: 1.4,
      marginBottom: 'var(--space-6)'
    }
  }, q.q), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gap: 10
    }
  }, q.opts.map((o, idx) => /*#__PURE__*/React.createElement(QuizOption, {
    key: o,
    letter: 'ABCD'[idx],
    state: revealed ? idx === q.correct ? 'correct' : idx === sel ? 'incorrect' : 'idle' : idx === sel ? 'selected' : 'idle',
    onClick: () => !revealed && setSel(idx)
  }, o))), revealed && /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 'var(--space-5)',
      padding: '12px 14px',
      background: 'var(--surface-sunken)',
      borderRadius: 'var(--radius-md)',
      fontSize: 14,
      color: 'var(--text-body)'
    }
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: 'var(--text-heading)'
    }
  }, "Why:"), " ", q.explain), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      marginTop: 'var(--space-6)'
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "ghost",
    onClick: onExit
  }, "Exit round"), revealed ? /*#__PURE__*/React.createElement(Button, {
    onClick: next
  }, i + 1 >= BANK.length ? 'See results' : 'Next question') : /*#__PURE__*/React.createElement(Button, {
    disabled: sel === null,
    onClick: submit
  }, "Submit answer"))));
}
Object.assign(window, {
  Practice,
  BANK
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/web_app/Practice.jsx", error: String((e && e.message) || e) }); }

// ui_kits/web_app/Results.jsx
try { (() => {
function Results({
  score,
  total,
  onRetry,
  onHome
}) {
  const {
    Card,
    Button,
    Badge,
    StatTile,
    ProgressBar
  } = window.GMATStudyGuideDesignSystem_efe656;
  const pct = Math.round(score / total * 100);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 'var(--container-narrow)',
      margin: '0 auto',
      display: 'grid',
      gap: 'var(--space-6)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: 'center'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 56,
      fontWeight: 500,
      color: 'var(--brand-primary)'
    }
  }, score, " / ", total), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 'var(--text-xl)',
      fontWeight: 800,
      marginTop: 4
    }
  }, pct >= 67 ? 'Strong round.' : 'Good reps — keep going.'), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: '6px 0 0',
      color: 'var(--text-muted)'
    }
  }, "Quick 10 \xB7 Quant & Data Insights \xB7 5 min 12 sec")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: 'repeat(3,1fr)',
      gap: 'var(--space-4)'
    }
  }, /*#__PURE__*/React.createElement(StatTile, {
    label: "Accuracy",
    value: pct + '%'
  }), /*#__PURE__*/React.createElement(StatTile, {
    label: "Avg. pace",
    value: "1:44",
    delta: "\u22120:08"
  }), /*#__PURE__*/React.createElement(StatTile, {
    label: "Est. score",
    value: "645",
    delta: "+5"
  })), /*#__PURE__*/React.createElement(Card, {
    title: "This round"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gap: 8
    }
  }, window.BANK.map((q, idx) => /*#__PURE__*/React.createElement("div", {
    key: idx,
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 12,
      padding: '10px 12px',
      background: 'var(--surface-sunken)',
      borderRadius: 'var(--radius-md)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 12,
      color: 'var(--text-muted)',
      width: 18
    }
  }, idx + 1), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      fontSize: 14,
      color: 'var(--text-heading)',
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      whiteSpace: 'nowrap'
    }
  }, q.q), /*#__PURE__*/React.createElement(Badge, {
    tone: "neutral"
  }, q.tag), /*#__PURE__*/React.createElement(Badge, {
    tone: idx < 2 ? 'success' : 'error'
  }, idx < 2 ? 'Correct' : 'Missed'))))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'center',
      gap: 'var(--space-3)'
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    onClick: onHome
  }, "Back to dashboard"), /*#__PURE__*/React.createElement(Button, {
    onClick: onRetry
  }, "Practice again")));
}
Object.assign(window, {
  Results
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/web_app/Results.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.Tag = __ds_scope.Tag;

__ds_ns.Tooltip = __ds_scope.Tooltip;

__ds_ns.Dialog = __ds_scope.Dialog;

__ds_ns.ProgressBar = __ds_scope.ProgressBar;

__ds_ns.Toast = __ds_scope.Toast;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Checkbox = __ds_scope.Checkbox;

__ds_ns.IconButton = __ds_scope.IconButton;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Radio = __ds_scope.Radio;

__ds_ns.Select = __ds_scope.Select;

__ds_ns.Switch = __ds_scope.Switch;

__ds_ns.Dropdown = __ds_scope.Dropdown;

__ds_ns.Tabs = __ds_scope.Tabs;

__ds_ns.Flashcard = __ds_scope.Flashcard;

__ds_ns.QuizOption = __ds_scope.QuizOption;

__ds_ns.StatTile = __ds_scope.StatTile;

})();
