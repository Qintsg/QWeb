/**
 * 注册 Material Web Components。
 *
 * :project: QWeb
 * :file: material-setup.ts
 * :author: Qintsg
 * :date: 2026-05-17 00:00
 */
import "@material/web/button/elevated-button.js"
import "@material/web/button/filled-button.js"
import "@material/web/button/filled-tonal-button.js"
import "@material/web/button/outlined-button.js"
import "@material/web/button/text-button.js"
import "@material/web/checkbox/checkbox.js"
import "@material/web/chips/assist-chip.js"
import "@material/web/chips/filter-chip.js"
import "@material/web/dialog/dialog.js"
import "@material/web/divider/divider.js"
import "@material/web/fab/fab.js"
import "@material/web/icon/icon.js"
import "@material/web/iconbutton/icon-button.js"
import "@material/web/list/list.js"
import "@material/web/list/list-item.js"
import "@material/web/menu/menu.js"
import "@material/web/menu/menu-item.js"
import "@material/web/progress/circular-progress.js"
import "@material/web/progress/linear-progress.js"
import "@material/web/radio/radio.js"
import "@material/web/select/outlined-select.js"
import "@material/web/select/select-option.js"
import "@material/web/switch/switch.js"
import "@material/web/tabs/primary-tab.js"
import "@material/web/tabs/tabs.js"
import "@material/web/textfield/outlined-text-field.js"
import "@material/web/typography/md-typescale-styles.js"

/**
 * 保持 Material Web 组件注册入口可显式调用。
 *
 * :return: 无返回值。
 */
export function setupMaterialDesignSystem(): void {
  // 仅导入 custom elements 即完成注册；函数用于让 main.ts 的初始化语义保持清晰。
}
