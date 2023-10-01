"use strict";
(self["webpackChunkjupyterlab_tpt"] = self["webpackChunkjupyterlab_tpt"] || []).push([["lib_index_js"],{

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
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! jupyterlab-celltagsclasses */ "./node_modules/jupyterlab-celltagsclasses/lib/metadata.js");
/* harmony import */ var jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! jupyterlab-celltagsclasses */ "./node_modules/jupyterlab-celltagsclasses/lib/apply_on_cells.js");
/*
 * for attaching keybindings later on, see
 * https://towardsdatascience.com/how-to-customize-jupyterlab-keyboard-shortcuts-72321f73753d
 */



// md_clean may be broken


/*
in order to have consistent behaviour between
classic notebook (with the hide-input extension enabled)
and jupyter book, we manage consistently
* the metadata.hide_input attribute
* the 'hide-input' tag
*/
const _set_hide = (cell, hidden, input_output) => {
    if (hidden) {
        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_set)(cell, `hide_${input_output}`, true);
        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_insert)(cell, 'tags', `hide-${input_output}`);
    }
    else {
        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_unset)(cell, `hide_${input_output}`);
        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_remove)(cell, 'tags', `hide-${input_output}`);
    }
};
const _toggle_hide = (cell, input_output) => {
    if ((0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_get)(cell, `tags.hide-${input_output}`)) {
        _set_hide(cell, false, input_output);
    }
    else {
        _set_hide(cell, true, input_output);
    }
};
const set_hide_input = (cell, hidden) => _set_hide(cell, hidden, 'input');
const set_hide_output = (cell, hidden) => _set_hide(cell, hidden, 'output');
const toggle_hide_input = (cell) => _toggle_hide(cell, 'input');
const toggle_hide_output = (cell) => _toggle_hide(cell, 'output');
// this is specific to the web course, where we use a toolset with functions
// that have this in their name
const NEEDLE = 'tools.sample_from';
const set_hide_input_needle = (cell, hidden) => {
    // ignore text cells
    if (cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__.CodeCell) {
        // need to access the cell model
        const model = cell.model;
        if (model.sharedModel.getSource().toLowerCase().indexOf(NEEDLE) !== -1) {
            set_hide_input(cell, hidden);
        }
    }
};
// use depth=0 to remove
const make_text_and_insert_section = (notebook, depth) => {
    // console.log("make_text_and_insert_section", depth)
    _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.NotebookActions.changeCellType(notebook, 'markdown');
    const activeCell = notebook === null || notebook === void 0 ? void 0 : notebook.activeCell;
    if (activeCell === undefined) {
        return;
    }
    const model = activeCell === null || activeCell === void 0 ? void 0 : activeCell.model;
    if (model === undefined) {
        return;
    }
    // remove starting #'s if any
    for (let i = 4; i > 0; i--) {
        model.sharedModel.setSource(model.sharedModel.getSource().replace('#'.repeat(i) + ' ', ''));
    }
    if (depth === 0) {
        return;
    }
    model.sharedModel.setSource(`${'#'.repeat(depth)} ${model.sharedModel.getSource()}`);
};
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
const toggle_tag = (cell, tag) => {
    if ((0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_get)(cell, 'tags', tag)) {
        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_remove)(cell, 'tags', tag);
    }
    else {
        (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_insert)(cell, 'tags', tag);
    }
};
/**
 * Initialization data for the jupyterlab-tpt extension.
 */
const plugin = {
    id: 'jupyterlab-tpt:plugin',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker],
    activate: (app, palette, notebookTracker) => {
        console.log('extension jupyterlab-tpt is activating');
        // console.log('ICommandPalette', palette)
        // console.log('INotebookTracker', notebookTracker)
        // the addCommand would accept the following
        // isEnabled: () => true,
        // isVisible: () => true,
        // iconClass: 'some-css-icon-class',
        // also we could pass args to execute, but in the hide-input case
        // it does not work well as we need distinct labels depending on the args
        // https://lumino.readthedocs.io/en/1.x/api/commands/interfaces/commandregistry.ikeybindingoptions.html
        // The supported modifiers are: Accel, Alt, Cmd, Ctrl, and Shift. The Accel
        // modifier is translated to Cmd on Mac and Ctrl on all other platforms. The
        // Cmd modifier is ignored on non-Mac platforms.
        // Alt is option on mac
        let command;
        // Option-Command-9 = toggle (hide-input) on all selected cells
        // Ctrl-Alt-9 = show (wrt hide-input) on all selected cells
        command = 'convenience:hide-input';
        app.commands.addCommand(command, {
            label: 'hide input for all selected cells',
            execute: () => (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.Scope.Multiple, (cell) => set_hide_input(cell, true))
        });
        palette.addItem({ command, category: 'Convenience' });
        command = 'convenience:show-input';
        app.commands.addCommand(command, {
            label: 'show input for all selected cells',
            execute: () => (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.Scope.Multiple, (cell) => set_hide_input(cell, false))
        });
        palette.addItem({ command, category: 'Convenience' });
        app.commands.addKeyBinding({ command, keys: ['Ctrl Alt 9'], selector: '.jp-Notebook' });
        command = 'convenience:toggle-show-input';
        app.commands.addCommand(command, {
            label: 'toggle show input for all selected cells',
            execute: () => (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.Scope.Multiple, (cell) => toggle_hide_input(cell))
        });
        palette.addItem({ command, category: 'Convenience' });
        app.commands.addKeyBinding({ command, keys: ['Alt Cmd 9'], selector: '.jp-Notebook' });
        command = 'convenience:hide-output';
        app.commands.addCommand(command, {
            label: 'hide output for all selected cells',
            execute: () => (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.Scope.Multiple, (cell) => set_hide_output(cell, true))
        });
        palette.addItem({ command, category: 'Convenience' });
        command = 'convenience:show-output';
        app.commands.addCommand(command, {
            label: 'show output for all selected cells',
            execute: () => (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.Scope.Multiple, (cell) => set_hide_output(cell, false))
        });
        palette.addItem({ command, category: 'Convenience' });
        app.commands.addKeyBinding({ command, keys: ['Ctrl Alt 0'], selector: '.jp-Notebook' });
        command = 'convenience:toggle-show-output';
        app.commands.addCommand(command, {
            label: 'toggle show output for all selected cells',
            execute: () => (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.Scope.Multiple, (cell) => toggle_hide_output(cell))
        });
        palette.addItem({ command, category: 'Convenience' });
        app.commands.addKeyBinding({ command, keys: ['Alt Cmd 0'], selector: '.jp-Notebook' });
        command = 'convenience:hide-input-all-samples';
        app.commands.addCommand(command, {
            label: `hide input for all code cells that contain ${NEEDLE}`,
            execute: () => (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.Scope.All, (cell) => set_hide_input_needle(cell, true))
        });
        palette.addItem({ command, category: 'Convenience' });
        app.commands.addKeyBinding({ command, keys: ['Alt Cmd 8'], selector: '.jp-Notebook' });
        command = 'convenience:show-input-all-samples';
        app.commands.addCommand(command, {
            label: `show input for all code cells that contain ${NEEDLE}`,
            execute: () => (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.Scope.All, (cell) => set_hide_input_needle(cell, false))
        });
        palette.addItem({ command, category: 'Convenience' });
        app.commands.addKeyBinding({ command, keys: ['Ctrl Alt 8'], selector: '.jp-Notebook' });
        command = 'convenience:metadata-clean-selected';
        app.commands.addCommand(command, {
            label: `clean metadata for all selected cells`,
            execute: () => (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.Scope.Multiple, clean_cell_metadata)
        });
        palette.addItem({ command, category: 'Convenience' });
        app.commands.addKeyBinding({ command, keys: ['Alt Cmd 7'], selector: '.jp-Notebook' });
        command = 'convenience:metadata-clean-all';
        app.commands.addCommand(command, {
            label: `clean metadata for all cells`,
            execute: () => (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.Scope.All, clean_cell_metadata)
        });
        palette.addItem({ command, category: 'Convenience' });
        app.commands.addKeyBinding({ command, keys: ['Ctrl Alt 7'], selector: '.jp-Notebook' });
        // Ctrl-0 to Ctrl-4 to set markdown sections
        for (let depth = 0; depth < 5; depth++) {
            command = `convenience:section-level-${depth}`;
            app.commands.addCommand(command, {
                label: `active cell becomes section level ${depth}`,
                execute: () => {
                    var _a;
                    const notebook = (_a = notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                    if (notebook === undefined) {
                        return;
                    }
                    make_text_and_insert_section(notebook, depth);
                }
            });
            palette.addItem({ command, category: 'Convenience' });
            app.commands.addKeyBinding({ command, keys: [`Ctrl ${depth}`], selector: '.jp-Notebook' });
        }
        // render-all-cells - unrender-all-cells (markdown actually)
        const unrender_markdown = (cell) => {
            if (cell.model.type !== 'markdown') {
                return;
            }
            cell.rendered = false;
        };
        command = 'notebook:unrender-all-markdown';
        app.commands.addCommand(command, {
            label: 'unrender all markdown cells',
            execute: () => (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.Scope.All, unrender_markdown)
        });
        palette.addItem({ command, category: 'Convenience' });
        // control-e means end of ine if in edit mode
        app.commands.addKeyBinding({ command, keys: ['Ctrl E'], selector: '.jp-Notebook.jp-mod-commandMode' });
        app.commands.addKeyBinding({ command: 'notebook:render-all-markdown', keys: ['Ctrl W'], selector: '.jp-Notebook' });
        // this is actually lowercase u and d, would need an explicit Shift otherwise
        app.commands.addKeyBinding({ command: 'notebook:move-cell-up', keys: ['U'], selector: '.jp-Notebook.jp-mod-commandMode' });
        app.commands.addKeyBinding({ command: 'notebook:move-cell-down', keys: ['D'], selector: '.jp-Notebook.jp-mod-commandMode' });
        command = 'convenience:toggle-raises-exception';
        app.commands.addCommand(command, {
            label: 'toggle raises-exception for all selected cells',
            execute: () => (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.Scope.Multiple, (cell) => toggle_tag(cell, 'raises-exception')),
        });
        palette.addItem({ command, category: 'Convenience' });
        app.commands.addKeyBinding({ command, keys: ['Alt Cmd 6'], selector: '.jp-Notebook' });
        command = 'convenience:set-raises-exception';
        app.commands.addCommand(command, {
            label: 'set raises-exception for all selected cells',
            execute: () => (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.Scope.Multiple, (cell) => (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_3__.md_insert)(cell, 'tags', 'raises-exception')),
        });
        palette.addItem({ command, category: 'Convenience' });
        app.commands.addKeyBinding({ command, keys: ['Ctrl Alt 6'], selector: '.jp-Notebook' });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.5b717e8908bd644bc806.js.map