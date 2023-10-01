"use strict";
(self["webpackChunkjupyterlab_courselevels"] = self["webpackChunkjupyterlab_courselevels"] || []).push([["lib_index_js"],{

/***/ "./lib/admonitions.js":
/*!****************************!*\
  !*** ./lib/admonitions.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   toggle_admonition: () => (/* binding */ toggle_admonition)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* eslint-disable prettier/prettier */

const FENCE = '````';
/* works on the active cell */
const toggle_admonition = (notebook, admonition) => {
    const activeCell = notebook === null || notebook === void 0 ? void 0 : notebook.activeCell;
    if (activeCell === undefined) {
        return;
    }
    const model = activeCell === null || activeCell === void 0 ? void 0 : activeCell.model;
    if (model === undefined) {
        return;
    }
    _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.changeCellType(notebook, 'markdown');
    let cell_source = model.sharedModel.getSource();
    // remove trailing newlines
    while (cell_source.endsWith('\n')) {
        cell_source = cell_source.slice(0, -1);
    }
    // does it start with an admonition?
    const turning_off = cell_source.startsWith(FENCE);
    console.debug('admonition: turning_off', turning_off);
    // a function that removes any initial white line, and any trailing white line
    // a line is considered white if it is empty or only contains whitespace
    const tidy = (dirty) => {
        const lines = dirty.split('\n');
        while (lines.length != 0 && lines[0].match(/^\s*$/)) {
            lines.shift();
        }
        while (lines.length != 0 && lines[lines.length - 1].match(/^\s*$/)) {
            lines.pop();
        }
        return lines.join('\n');
    };
    let new_source;
    if (turning_off) {
        new_source = tidy(cell_source
            .replace(RegExp(`^${FENCE} *{[a-zA-Z]+}`), '')
            .replace(RegExp(`\n${FENCE}$`), ''));
    }
    else {
        new_source = `${FENCE}{${admonition}}\n${tidy(cell_source)}\n${FENCE}`;
    }
    model.sharedModel.setSource(new_source);
};


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! jupyterlab-celltagsclasses */ "webpack/sharing/consume/default/jupyterlab-celltagsclasses/jupyterlab-celltagsclasses");
/* harmony import */ var jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _admonitions__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./admonitions */ "./lib/admonitions.js");
/*
 * for attaching keybindings later on, see
 * https://towardsdatascience.com/how-to-customize-jupyterlab-keyboard-shortcuts-72321f73753d
 */







// md_clean may be broken
// import { md_set, , md_insert, md_remove } from 'jupyterlab-celltagsclasses'
const clean_cell_metadata = (cell) => {
    console.log("Cleaning metadata for cell", cell);
    const editable = cell.model.getMetadata('editable');
    if (editable === true) {
        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_unset)(cell, 'editable');
    }
    const tags = cell.model.getMetadata('tags');
    if ((tags === null || tags === void 0 ? void 0 : tags.length) === 0) {
        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_unset)(cell, 'tags');
    }
    const slide_type = (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_get)(cell, 'slideshow.slide_type');
    if (slide_type === '') {
        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_unset)(cell, 'slideshow.slide_type');
    }
    const slideshow = (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_get)(cell, 'slideshow');
    if ((slideshow !== undefined) && (JSON.stringify(slideshow) == '{}')) {
        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_unset)(cell, 'slideshow');
    }
    const user_expressions = (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_get)(cell, 'user_expressions');
    if ((user_expressions === null || user_expressions === void 0 ? void 0 : user_expressions.length) === 0) {
        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_unset)(cell, 'user_expressions');
    }
};
const plugin = {
    id: 'jupyterlab-courselevels:plugin',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker],
    activate: (app, palette, notebookTracker) => {
        console.log('extension jupyterlab-courselevels is activating');
        // https://lumino.readthedocs.io/en/1.x/api/commands/interfaces/commandregistry.ikeybindingoptions.html
        // The supported modifiers are: Accel, Alt, Cmd, Ctrl, and Shift. The Accel
        // modifier is translated to Cmd on Mac and Ctrl on all other platforms. The
        // Cmd modifier is ignored on non-Mac platforms.
        // Alt is option on mac
        const cell_toggle_level = (cell, level) => {
            switch (level) {
                case 'basic':
                    if ((0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_has)(cell, 'tags', 'level_basic')) {
                        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_remove)(cell, 'tags', 'level_basic');
                    }
                    else {
                        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_insert)(cell, 'tags', 'level_basic');
                        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_remove)(cell, 'tags', 'level_intermediate');
                        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_remove)(cell, 'tags', 'level_advanced');
                    }
                    break;
                case 'intermediate':
                    if ((0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_has)(cell, 'tags', 'level_intermediate')) {
                        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_remove)(cell, 'tags', 'level_intermediate');
                    }
                    else {
                        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_remove)(cell, 'tags', 'level_basic');
                        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_insert)(cell, 'tags', 'level_intermediate');
                        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_remove)(cell, 'tags', 'level_advanced');
                    }
                    break;
                case 'advanced':
                    if ((0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_has)(cell, 'tags', 'level_advanced')) {
                        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_remove)(cell, 'tags', 'level_advanced');
                    }
                    else {
                        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_remove)(cell, 'tags', 'level_basic');
                        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_remove)(cell, 'tags', 'level_intermediate');
                        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_insert)(cell, 'tags', 'level_advanced');
                    }
                    break;
                default:
                    (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_remove)(cell, 'tags', 'level_basic');
                    (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_remove)(cell, 'tags', 'level_intermediate');
                    (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_remove)(cell, 'tags', 'level_advanced');
            }
        };
        const toggle_level = (level) => {
            (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.Scope.Active, (cell) => {
                cell_toggle_level(cell, level);
            });
        };
        let command;
        for (const [level, key] of [
            ['basic', 'Ctrl X'],
            ['intermediate', 'Ctrl Y'],
            ['advanced', 'Ctrl Z'],
        ]) {
            command = `courselevels:toggle-level-${level}`;
            app.commands.addCommand(command, {
                label: `toggle ${level} level`,
                execute: () => toggle_level(level)
            });
            palette.addItem({ command, category: 'CourseLevels' });
            app.commands.addKeyBinding({ command, keys: ['Ctrl \\', key], selector: '.jp-Notebook' });
        }
        const toggle_frame = () => {
            (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.Scope.Active, (cell) => {
                (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_toggle)(cell, 'tags', 'framed_cell');
            });
        };
        command = 'courselevels:toggle-frame';
        app.commands.addCommand(command, {
            label: 'toggle frame',
            execute: () => toggle_frame()
        });
        palette.addItem({ command, category: 'CourseLevels' });
        app.commands.addKeyBinding({ command, keys: ['Ctrl \\', 'Ctrl M'], selector: '.jp-Notebook' });
        const toggle_licence = () => {
            (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.Scope.Active, (cell) => {
                (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_toggle)(cell, 'tags', 'licence');
            });
        };
        command = 'courselevels:toggle-licence';
        app.commands.addCommand(command, {
            label: 'toggle licence',
            execute: () => toggle_licence()
        });
        palette.addItem({ command, category: 'CourseLevels' });
        app.commands.addKeyBinding({ command, keys: ['Ctrl \\', 'Ctrl L'], selector: '.jp-Notebook' });
        command = 'courselevels:metadata-clean-selected';
        app.commands.addCommand(command, {
            label: `clean metadata for all selected cells`,
            execute: () => (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.Scope.Multiple, clean_cell_metadata)
        });
        palette.addItem({ command, category: 'Convenience' });
        app.commands.addKeyBinding({ command, keys: ['Alt Cmd 7'], selector: '.jp-Notebook' });
        command = 'convenience:metadata-clean-all';
        app.commands.addCommand(command, {
            label: `clean metadata for all cells`,
            execute: () => (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.Scope.All, clean_cell_metadata)
        });
        palette.addItem({ command, category: 'Convenience' });
        app.commands.addKeyBinding({ command, keys: ['Ctrl Alt 7'], selector: '.jp-Notebook' });
        // the buttons in the toolbar
        const find_spacer = (panel) => {
            let index = 0;
            for (const child of panel.toolbar.children()) {
                if (child.node.classList.contains('jp-Toolbar-spacer')) {
                    return index;
                }
                else {
                    index += 1;
                }
            }
            return 0;
        };
        class BasicButton {
            createNew(panel, context) {
                const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
                    className: 'courselevels-button',
                    iconClass: 'far fa-hand-pointer',
                    onClick: () => toggle_level('basic'),
                    tooltip: 'Toggle basic level',
                });
                // compute where to insert it
                const index = find_spacer(panel);
                panel.toolbar.insertItem(index, 'basicLevel', button);
                return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_2__.DisposableDelegate(() => {
                    button.dispose();
                });
            }
        }
        app.docRegistry.addWidgetExtension('Notebook', new BasicButton());
        class IntermediateButton {
            createNew(panel, context) {
                const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
                    className: 'courselevels-button',
                    iconClass: 'far fa-hand-peace',
                    onClick: () => toggle_level('intermediate'),
                    tooltip: 'Toggle intermediate level',
                });
                // compute where to insert it
                const index = find_spacer(panel);
                panel.toolbar.insertItem(index, 'intermediateLevel', button);
                return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_2__.DisposableDelegate(() => {
                    button.dispose();
                });
            }
        }
        app.docRegistry.addWidgetExtension('Notebook', new IntermediateButton());
        class AdvancedButton {
            createNew(panel, context) {
                const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
                    className: 'courselevels-button',
                    iconClass: 'far fa-hand-spock',
                    onClick: () => toggle_level('advanced'),
                    tooltip: 'Toggle advanced level',
                });
                // compute where to insert it
                const index = find_spacer(panel);
                panel.toolbar.insertItem(index, 'advancedLevel', button);
                return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_2__.DisposableDelegate(() => {
                    button.dispose();
                });
            }
        }
        app.docRegistry.addWidgetExtension('Notebook', new AdvancedButton());
        class FrameButton {
            createNew(panel, context) {
                const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
                    className: 'courselevels-button',
                    iconClass: 'fas fa-crop-alt',
                    onClick: () => toggle_frame(),
                    tooltip: 'Toggle frame around cell',
                });
                // compute where to insert it
                const index = find_spacer(panel);
                panel.toolbar.insertItem(index, 'frameLevel', button);
                return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_2__.DisposableDelegate(() => {
                    button.dispose();
                });
            }
        }
        app.docRegistry.addWidgetExtension('Notebook', new FrameButton());
        // admonitions
        for (const [name, key] of [
            ['admonition', 'Ctrl A'],
            ['tip', 'Ctrl T'],
            ['note', 'Ctrl N'],
            ['attention', null],
            ['caution', null],
            ['danger', null],
            ['error', null],
            ['hint', null],
            ['important', null],
            ['seealso', null],
            ['warning', null],
        ]) {
            // need to cast because name is typed as string | null ?!?
            const admonition = name;
            command = 'courselevels:toggle-admonition';
            let label = 'toggle admonition';
            if (admonition !== 'admonition') {
                command += `-${admonition}`;
                label += ` ${admonition}`;
            }
            app.commands.addCommand(command, {
                label,
                execute: () => {
                    var _a;
                    const notebook = (_a = notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                    if (notebook === undefined) {
                        return;
                    }
                    (0,_admonitions__WEBPACK_IMPORTED_MODULE_4__.toggle_admonition)(notebook, admonition);
                }
            });
            palette.addItem({ command, category: 'CourseLevels' });
            if (key !== null) {
                app.commands.addKeyBinding({ command, keys: ['Ctrl \\', key], selector: '.jp-Notebook' });
            }
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.b75bb00c89a217164bbc.js.map