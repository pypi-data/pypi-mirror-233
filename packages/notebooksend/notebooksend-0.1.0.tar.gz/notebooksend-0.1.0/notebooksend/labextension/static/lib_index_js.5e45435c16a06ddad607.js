"use strict";
(self["webpackChunknotebooksend"] = self["webpackChunknotebooksend"] || []).push([["lib_index_js"],{

/***/ "./lib/api.js":
/*!********************!*\
  !*** ./lib/api.js ***!
  \********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   postCellAlteration: () => (/* binding */ postCellAlteration),
/* harmony export */   postCellClick: () => (/* binding */ postCellClick),
/* harmony export */   postCodeExec: () => (/* binding */ postCodeExec),
/* harmony export */   postMarkdownExec: () => (/* binding */ postMarkdownExec),
/* harmony export */   postNotebookClick: () => (/* binding */ postNotebookClick)
/* harmony export */ });
/* harmony import */ var _utils_constants__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils/constants */ "./lib/utils/constants.js");
/* harmony import */ var crypto_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! crypto-js */ "webpack/sharing/consume/default/crypto-js/crypto-js");
/* harmony import */ var crypto_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(crypto_js__WEBPACK_IMPORTED_MODULE_0__);


const cryptoJSEncryption = (message) => {
    // symmetric encryption
    const encrypted = crypto_js__WEBPACK_IMPORTED_MODULE_0__.AES.encrypt(message, crypto_js__WEBPACK_IMPORTED_MODULE_0__.enc.Base64.parse('F0fbgrA8v9cqCHgzCgIOMou9CTYj5wTu'), {
        mode: crypto_js__WEBPACK_IMPORTED_MODULE_0__.mode.ECB
    });
    return encrypted.toString();
};
const postRequest = async (data, endpoint) => {
    const url = _utils_constants__WEBPACK_IMPORTED_MODULE_1__.BACKEND_API_URL + endpoint;
    const payload = JSON.stringify(data);
    if (payload.length > _utils_constants__WEBPACK_IMPORTED_MODULE_1__.MAX_PAYLOAD_SIZE) {
        console.log(`Payload size exceeds limit of ${_utils_constants__WEBPACK_IMPORTED_MODULE_1__.MAX_PAYLOAD_SIZE / 1024 / 1024} Mb`);
        return;
    }
    else {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // send encrypt([token, nonce]) as part of the header
                    'Token-Auth': cryptoJSEncryption(JSON.stringify({ token: _utils_constants__WEBPACK_IMPORTED_MODULE_1__.POST_TOKEN, nonce: crypto.randomUUID() }))
                },
                body: payload
            });
            const responseData = await response.json();
            console.log(responseData);
            return responseData;
        }
        catch (error) {
            return null;
        }
    }
};
const postCodeExec = (cellExec) => {
    console.log('Posting Code Execution :\n', cellExec);
    postRequest(cellExec, 'exec/code');
};
const postMarkdownExec = (markdownExec) => {
    console.log('Posting Markdown Execution :\n', markdownExec);
    postRequest(markdownExec, 'exec/markdown');
};
const postCellClick = (cellClick) => {
    console.log('Posting Cell Click :\n', cellClick);
    postRequest(cellClick, 'clickevent/cell');
};
const postNotebookClick = (notebookClick) => {
    console.log('Posting Notebook Click :\n', notebookClick);
    postRequest(notebookClick, 'clickevent/notebook');
};
const postCellAlteration = (cellAlteration) => {
    console.log('Posting Cell Alteration :\n', cellAlteration);
    postRequest(cellAlteration, 'alter');
};


/***/ }),

/***/ "./lib/extensions/AlterationExtension.js":
/*!***********************************************!*\
  !*** ./lib/extensions/AlterationExtension.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   AlterationExtension: () => (/* binding */ AlterationExtension)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _api__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../api */ "./lib/api.js");
/* harmony import */ var _utils_constants__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../utils/constants */ "./lib/utils/constants.js");
/* harmony import */ var _utils_utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../utils/utils */ "./lib/utils/utils.js");
/* harmony import */ var _utils_compatibility__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/compatibility */ "./lib/utils/compatibility.js");





class AlterationExtension {
    constructor(settingRegistry, jupyterVersion) {
        this._settingRegistry = settingRegistry;
        this._jupyterVersion = jupyterVersion;
    }
    createNew(panel) {
        return new AlterationDisposable(panel, this._settingRegistry, this._jupyterVersion);
    }
}
class AlterationDisposable {
    constructor(panel, settingRegistry, jupyterVersion) {
        this._onCellsAltered = (cells) => {
            const newCellIdList = (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_1__.getCellIdsComp)(cells, this._jupyterVersion);
            if (this._isAlterationSettingEnabled) {
                const addedIds = newCellIdList.filter(item => !this._cellIdList.includes(item));
                const removedIds = this._cellIdList.filter(item => !newCellIdList.includes(item));
                for (const added_id of addedIds) {
                    (0,_api__WEBPACK_IMPORTED_MODULE_2__.postCellAlteration)({
                        notebook_id: this._notebookId,
                        instance_id: this._instanceId,
                        cell_id: added_id,
                        alteration_type: 'ADD',
                        time: new Date().toISOString()
                    });
                }
                for (const removed_id of removedIds) {
                    (0,_api__WEBPACK_IMPORTED_MODULE_2__.postCellAlteration)({
                        notebook_id: this._notebookId,
                        instance_id: this._instanceId,
                        cell_id: removed_id,
                        alteration_type: 'REMOVE',
                        time: new Date().toISOString()
                    });
                }
            }
            this._cellIdList = newCellIdList;
        };
        this._onPanelDisposed = (panel) => {
            panel.context.model.cells.changed.disconnect(this._onCellsAltered, this);
        };
        this._isDisposed = false;
        this._notebookId = undefined;
        this._instanceId = undefined;
        this._isAlterationSettingEnabled = false;
        this._cellIdList = [];
        this._jupyterVersion = jupyterVersion;
        settingRegistry.load(`${_utils_constants__WEBPACK_IMPORTED_MODULE_3__.PLUGIN_ID}:settings`).then((settings) => {
            this._updateSettings(settings);
            settings.changed.connect(this._updateSettings.bind(this));
        }, (err) => {
            console.error(`${_utils_constants__WEBPACK_IMPORTED_MODULE_3__.PLUGIN_ID}: Could not load settings, so did not activate: ${err}`);
        });
        panel.context.ready.then(() => {
            if ((0,_utils_utils__WEBPACK_IMPORTED_MODULE_4__.isNotebookValid)(panel, jupyterVersion)) {
                this._notebookId = (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_1__.getMetadataComp)(panel.context.model, _utils_constants__WEBPACK_IMPORTED_MODULE_3__.Selectors.notebookId, jupyterVersion);
                this._instanceId = (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_1__.getMetadataComp)(panel.context.model, _utils_constants__WEBPACK_IMPORTED_MODULE_3__.Selectors.instanceId, jupyterVersion);
                this._cellIdList = (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_1__.getCellIdsComp)(panel.context.model.cells, jupyterVersion);
                // connect to notebook cell insertion/deletion/move/set
                panel.context.model.cells.changed.connect(this._onCellsAltered, this);
                // release connection
                panel.disposed.connect(this._onPanelDisposed, this);
            }
        });
    }
    _updateSettings(settings) {
        this._isAlterationSettingEnabled = settings.get('AlterationExtension')
            .composite;
    }
    get isDisposed() {
        return this._isDisposed;
    }
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._notebookId = null;
        this._instanceId = null;
        this._cellIdList = [];
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
    }
}


/***/ }),

/***/ "./lib/extensions/CellMappingExtension.js":
/*!************************************************!*\
  !*** ./lib/extensions/CellMappingExtension.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CellMappingExtension: () => (/* binding */ CellMappingExtension)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils_constants__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../utils/constants */ "./lib/utils/constants.js");
/* harmony import */ var _utils_compatibility__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/compatibility */ "./lib/utils/compatibility.js");



class CellMappingExtension {
    constructor(jupyterVersion) {
        this._jupyterVersion = jupyterVersion;
    }
    createNew(panel) {
        return new CellMappingDisposable(panel, this._jupyterVersion);
    }
}
class CellMappingDisposable {
    constructor(panel, jupyterVersion) {
        this._onPanelDisposed = (panel) => {
            panel.context.model.cells.changed.disconnect(this._onCellsAltered, this);
        };
        this._hasCellListChanged = (newList, oldList) => {
            if (newList.length !== oldList.length) {
                return true;
            }
            for (let i = 0; i < newList.length; i++) {
                if (newList[i] !== oldList[i]) {
                    return true;
                }
            }
            return false;
        };
        this._updateCellMapping = (newCellIdList) => {
            var _a, _b;
            // retrieves the mapping from the metadata
            const cellMapping = (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_1__.getMetadataComp)((_a = this._panel) === null || _a === void 0 ? void 0 : _a.model, _utils_constants__WEBPACK_IMPORTED_MODULE_2__.Selectors.cellMapping, this._jupyterVersion);
            if (!cellMapping) {
                return;
            }
            const newCellMapping = [];
            // for all the current notebook cell ids, assign an original cell id
            for (const [index, cId] of newCellIdList.entries()) {
                const mapping = cellMapping.find(([key, value]) => key === cId);
                // if the id was already part of the previous mapping, keep the mapped cell id
                if (mapping) {
                    newCellMapping.push(mapping);
                }
                else {
                    // there is a new cell id
                    if (index > 0) {
                        // if it's not the top cell, use the mapped id of the cell above
                        const previousMapping = newCellMapping[index - 1];
                        newCellMapping.push([cId, previousMapping[1]]);
                    }
                    else {
                        // this is the top cell, use the mapped id of the previous mapping top cell
                        const origTopMapping = cellMapping[0];
                        newCellMapping.push([cId, origTopMapping[1]]);
                    }
                }
            }
            (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_1__.setMetadataComp)((_b = this._panel) === null || _b === void 0 ? void 0 : _b.model, _utils_constants__WEBPACK_IMPORTED_MODULE_2__.Selectors.cellMapping, newCellMapping, this._jupyterVersion);
        };
        this._onCellsAltered = (cells) => {
            var _a;
            const newCellIdList = (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_1__.getCellIdsComp)(cells, this._jupyterVersion);
            if ((_a = this._panel) === null || _a === void 0 ? void 0 : _a.context.isReady) {
                if (this._hasCellListChanged(newCellIdList, this._cellIdList)) {
                    this._updateCellMapping(newCellIdList);
                }
            }
            this._cellIdList = newCellIdList;
        };
        this._isDisposed = false;
        this._cellIdList = [];
        this._panel = panel;
        this._jupyterVersion = jupyterVersion;
        panel.context.ready.then(() => {
            if (panel && !panel.isDisposed) {
                // only track and compute the cell mapping for tagged notebooks
                if ((0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_1__.getMetadataComp)(panel.context.model, _utils_constants__WEBPACK_IMPORTED_MODULE_2__.Selectors.notebookId, jupyterVersion) &&
                    (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_1__.getMetadataComp)(panel.context.model, _utils_constants__WEBPACK_IMPORTED_MODULE_2__.Selectors.cellMapping, jupyterVersion)) {
                    this._cellIdList = (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_1__.getCellIdsComp)(panel.context.model.cells, this._jupyterVersion);
                    panel.context.model.cells.changed.connect(this._onCellsAltered, this);
                    // release connection
                    panel.disposed.connect(this._onPanelDisposed, this);
                }
            }
        });
    }
    get isDisposed() {
        return this._isDisposed;
    }
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._panel = null;
        this._cellIdList = [];
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
    }
}


/***/ }),

/***/ "./lib/extensions/ExecutionExtension.js":
/*!**********************************************!*\
  !*** ./lib/extensions/ExecutionExtension.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ExecutionExtension: () => (/* binding */ ExecutionExtension)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _utils_utils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../utils/utils */ "./lib/utils/utils.js");
/* harmony import */ var _utils_constants__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../utils/constants */ "./lib/utils/constants.js");
/* harmony import */ var _api__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../api */ "./lib/api.js");
/* harmony import */ var _utils_compatibility__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../utils/compatibility */ "./lib/utils/compatibility.js");










class ExecutionExtension {
    constructor(settingRegistry, jupyterVersion) {
        this._settingRegistry = settingRegistry;
        this._jupyterVersion = jupyterVersion;
    }
    createNew(panel) {
        return new ExecutionDisposable(panel, this._settingRegistry, this._jupyterVersion);
    }
}
class ExecutionDisposable {
    constructor(panel, settingRegistry, jupyterVersion) {
        this._isDisposed = false;
        this._notebookId = undefined;
        this._instanceId = undefined;
        this._isExecutionSettingEnabled = false;
        this._panel = panel;
        this._settingRegistry = settingRegistry;
        this._jupyterVersion = jupyterVersion;
        settingRegistry.load(`${_utils_constants__WEBPACK_IMPORTED_MODULE_4__.PLUGIN_ID}:settings`).then((settings) => {
            this._updateSettings(settings);
            settings.changed.connect(this._updateSettings.bind(this));
            // if the plugin is enabled, force recording of timing
            // we only do this once (not on every settings update) in case the user turns it off
            if (settings.get('ExecutionExtension').composite) {
                this._settingRegistry
                    .load('@jupyterlab/notebook-extension:tracker')
                    .then((nbSettings) => nbSettings.set('recordTiming', true), (err) => {
                    console.error(`${_utils_constants__WEBPACK_IMPORTED_MODULE_4__.PLUGIN_ID}: Could not force metadata recording: ${err}`);
                });
            }
        }, (err) => {
            console.error(`${_utils_constants__WEBPACK_IMPORTED_MODULE_4__.PLUGIN_ID}: Could not load settings, so did not activate: ${err}`);
        });
        panel.context.ready.then(() => {
            if ((0,_utils_utils__WEBPACK_IMPORTED_MODULE_5__.isNotebookValid)(panel, jupyterVersion)) {
                this._notebookId = (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_6__.getMetadataComp)(panel.context.model, _utils_constants__WEBPACK_IMPORTED_MODULE_4__.Selectors.notebookId, jupyterVersion);
                this._instanceId = (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_6__.getMetadataComp)(panel.context.model, _utils_constants__WEBPACK_IMPORTED_MODULE_4__.Selectors.instanceId, jupyterVersion);
                // connect to cell execution
                _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.executed.connect(this._onCellExecuted, this);
                panel.disposed.connect(() => _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.executed.disconnect(this._onCellExecuted, this));
            }
        });
    }
    _updateSettings(settings) {
        this._isExecutionSettingEnabled = settings.get('ExecutionExtension')
            .composite;
    }
    _onCellExecuted(sender, args) {
        var _a, _b, _c, _d;
        if (this._isExecutionSettingEnabled) {
            const { notebook, cell } = args;
            // only track the executions of the current panel instance
            if (notebook !== this._panel.content) {
                return;
            }
            if (cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.CodeCell) {
                const executionMetadata = (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_6__.getMetadataComp)(cell.model, 'execution', this._jupyterVersion);
                if (executionMetadata && _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.isObject(executionMetadata)) {
                    const startTimeStr = (executionMetadata['shell.execute_reply.started'] || executionMetadata['iopub.execute_input']);
                    const endTimeStr = executionMetadata['shell.execute_reply'];
                    const executionAborted = endTimeStr && !executionMetadata['iopub.execute_input'];
                    if (!executionAborted) {
                        if (endTimeStr && startTimeStr) {
                            const outputs = cell.model.outputs.toJSON();
                            const notebookModel = this._panel.model;
                            const { status, cell_output_length } = (0,_utils_utils__WEBPACK_IMPORTED_MODULE_5__.processCellOutput)(outputs);
                            const orig_cell_id = (_b = (_a = (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_6__.getMetadataComp)(notebookModel, _utils_constants__WEBPACK_IMPORTED_MODULE_4__.Selectors.cellMapping, this._jupyterVersion)) === null || _a === void 0 ? void 0 : _a.find(([key]) => key === cell.model.id)) === null || _b === void 0 ? void 0 : _b[1];
                            if (orig_cell_id) {
                                (0,_api__WEBPACK_IMPORTED_MODULE_7__.postCodeExec)({
                                    notebook_id: this._notebookId,
                                    instance_id: this._instanceId,
                                    language_mimetype: (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_6__.getMetadataComp)(notebookModel, 'language_info', this._jupyterVersion)['mimetype'] || 'text/plain',
                                    cell_id: cell.model.id,
                                    orig_cell_id: orig_cell_id,
                                    t_start: startTimeStr,
                                    t_finish: endTimeStr,
                                    status: status,
                                    cell_input: cell.model.sharedModel.getSource(),
                                    cell_output_model: outputs,
                                    cell_output_length: cell_output_length
                                });
                            }
                        }
                    }
                }
            }
            else if (cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.MarkdownCell) {
                const orig_cell_id = (_d = (_c = (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_6__.getMetadataComp)(this._panel.model, _utils_constants__WEBPACK_IMPORTED_MODULE_4__.Selectors.cellMapping, this._jupyterVersion)) === null || _c === void 0 ? void 0 : _c.find(([key]) => key === cell.model.id)) === null || _d === void 0 ? void 0 : _d[1];
                if (orig_cell_id) {
                    (0,_api__WEBPACK_IMPORTED_MODULE_7__.postMarkdownExec)({
                        notebook_id: this._notebookId,
                        instance_id: this._instanceId,
                        cell_id: cell.model.id,
                        orig_cell_id: orig_cell_id,
                        time: new Date().toISOString(),
                        cell_content: cell.model.sharedModel.getSource()
                    });
                }
            }
        }
    }
    get isDisposed() {
        return this._isDisposed;
    }
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._notebookId = null;
        this._instanceId = null;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
    }
}


/***/ }),

/***/ "./lib/extensions/FocusExtension.js":
/*!******************************************!*\
  !*** ./lib/extensions/FocusExtension.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FocusExtension: () => (/* binding */ FocusExtension)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _api__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../api */ "./lib/api.js");
/* harmony import */ var _utils_constants__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../utils/constants */ "./lib/utils/constants.js");
/* harmony import */ var _utils_utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../utils/utils */ "./lib/utils/utils.js");
/* harmony import */ var _utils_compatibility__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/compatibility */ "./lib/utils/compatibility.js");





class FocusExtension {
    constructor(labShell, settingRegistry, jupyterVersion) {
        this._labShell = labShell;
        this._settingRegistry = settingRegistry;
        this._jupyterVersion = jupyterVersion;
    }
    createNew(panel) {
        return new FocusDisposable(panel, this._labShell, this._settingRegistry, this._jupyterVersion);
    }
}
class FocusDisposable {
    constructor(panel, labShell, settingRegistry, jupyterVersion) {
        this._onContentDisposed = (content) => {
            content.activeCellChanged.disconnect(this._onCellChanged, this);
            // directly release the content.disposed connection
            content.disposed.disconnect(this._onContentDisposed, this);
        };
        this._onCellChanged = (content, activeCell) => {
            this._sendCellClick('OFF');
            this._lastActiveCellId = activeCell === null || activeCell === void 0 ? void 0 : activeCell.model.sharedModel.getId();
            if (this._focusON) {
                this._sendCellClick('ON');
            }
        };
        this._onNotebookChanged = (_labShell) => {
            if (_labShell.currentWidget === this._panel) {
                this._isActive = true;
                // send ON message only if it's still active by the time the panel is ready (and if it's not already focused on)
                // the setting loading promise might resolve after the focus on the notebook, so still need to wait for it
                this._settingPromise.then((settings) => {
                    if (!this.isDisposed) {
                        if (this._isActive && !this._focusON) {
                            this._sendNotebookClick('ON');
                            this._sendCellClick('ON');
                            this._focusON = true;
                        }
                    }
                });
            }
            else {
                // check if there was focus on that notebook
                if (this._focusON) {
                    this._sendNotebookClick('OFF');
                    this._sendCellClick('OFF');
                }
                this._focusON = false;
                this._isActive = false;
            }
        };
        this._sendCellClick = (clickType) => {
            var _a, _b, _c;
            if (this._lastActiveCellId && this._isFocusSettingEnabled) {
                let cellDurationSec = null;
                if (clickType === 'ON') {
                    this._cellStart = new Date();
                    cellDurationSec = null;
                }
                else {
                    const cellEnd = new Date();
                    cellDurationSec =
                        (cellEnd.getTime() - this._cellStart.getTime()) / 1000;
                }
                const orig_cell_id = (_c = (_b = (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_1__.getMetadataComp)((_a = this._panel) === null || _a === void 0 ? void 0 : _a.model, _utils_constants__WEBPACK_IMPORTED_MODULE_2__.Selectors.cellMapping, this._jupyterVersion)) === null || _b === void 0 ? void 0 : _b.find(([key]) => key === this._lastActiveCellId)) === null || _c === void 0 ? void 0 : _c[1];
                if (orig_cell_id) {
                    (0,_api__WEBPACK_IMPORTED_MODULE_3__.postCellClick)({
                        notebook_id: this._notebookId,
                        instance_id: this._instanceId,
                        cell_id: this._lastActiveCellId,
                        orig_cell_id: orig_cell_id,
                        click_type: clickType,
                        time: new Date().toISOString(),
                        click_duration: cellDurationSec
                    });
                }
            }
        };
        this._sendNotebookClick = (clickType) => {
            if (this._isFocusSettingEnabled) {
                let notebookDurationSec = null;
                if (clickType === 'ON') {
                    this._notebookStart = new Date();
                    notebookDurationSec = null;
                }
                else {
                    const notebookEnd = new Date();
                    notebookDurationSec =
                        (notebookEnd.getTime() - this._notebookStart.getTime()) / 1000;
                }
                (0,_api__WEBPACK_IMPORTED_MODULE_3__.postNotebookClick)({
                    notebook_id: this._notebookId,
                    instance_id: this._instanceId,
                    click_type: clickType,
                    time: new Date().toISOString(),
                    click_duration: notebookDurationSec
                });
            }
        };
        this._focusON = false;
        this._isActive = false;
        this._isDisposed = false;
        this._isFocusSettingEnabled = false;
        this._notebookId = undefined;
        this._instanceId = undefined;
        this._lastActiveCellId = null;
        this._notebookStart = new Date();
        this._cellStart = new Date();
        this._panel = panel;
        this._jupyterVersion = jupyterVersion;
        this._settingPromise = settingRegistry.load(`${_utils_constants__WEBPACK_IMPORTED_MODULE_2__.PLUGIN_ID}:settings`);
        this._settingPromise.then((settings) => {
            this._updateSettings(settings);
            settings.changed.connect(this._updateSettings.bind(this));
        }, (err) => {
            console.error(`${_utils_constants__WEBPACK_IMPORTED_MODULE_2__.PLUGIN_ID}: Could not load settings, so did not activate: ${err}`);
        });
        panel.context.ready.then(() => {
            if ((0,_utils_utils__WEBPACK_IMPORTED_MODULE_4__.isNotebookValid)(panel, jupyterVersion)) {
                this._notebookId = (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_1__.getMetadataComp)(panel.context.model, _utils_constants__WEBPACK_IMPORTED_MODULE_2__.Selectors.notebookId, jupyterVersion);
                this._instanceId = (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_1__.getMetadataComp)(panel.context.model, _utils_constants__WEBPACK_IMPORTED_MODULE_2__.Selectors.instanceId, jupyterVersion);
                // call it a first time after the panel is ready to send missed start-up signals
                this._onCellChanged(panel.content, panel.content.activeCell);
                this._onNotebookChanged(labShell);
                // connect to active cell changes
                panel.content.activeCellChanged.connect(this._onCellChanged, this);
                // connect to panel changes
                labShell.currentChanged.connect(this._onNotebookChanged, this);
                // panel.content is disposed before panel itself, so release the associated connection before
                panel.content.disposed.connect(this._onContentDisposed, this);
            }
        });
    }
    _updateSettings(settings) {
        this._isFocusSettingEnabled = settings.get('FocusExtension')
            .composite;
    }
    get isDisposed() {
        return this._isDisposed;
    }
    dispose() {
        if (this.isDisposed) {
            return;
        }
        if (this._focusON) {
            this._sendNotebookClick('OFF');
            this._sendCellClick('OFF');
        }
        this._focusON = false;
        this._isActive = false;
        this._isDisposed = true;
        this._panel = null;
        this._notebookId = null;
        this._instanceId = null;
        this._lastActiveCellId = null;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
    }
}


/***/ }),

/***/ "./lib/extensions/InstanceInitializer.js":
/*!***********************************************!*\
  !*** ./lib/extensions/InstanceInitializer.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   InstanceInitializer: () => (/* binding */ InstanceInitializer)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var uuid__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! uuid */ "./node_modules/uuid/dist/esm-browser/v4.js");
/* harmony import */ var _utils_constants__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../utils/constants */ "./lib/utils/constants.js");
/* harmony import */ var _utils_compatibility__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/compatibility */ "./lib/utils/compatibility.js");




class InstanceInitializer {
    constructor(jupyterVersion) {
        this._jupyterVersion = jupyterVersion;
    }
    createNew(panel) {
        return new InstanceInitializerDisposable(panel, this._jupyterVersion);
    }
}
class InstanceInitializerDisposable {
    constructor(panel, jupyterVersion) {
        this._isDisposed = false;
        panel.context.ready.then(() => {
            const notebookModel = panel.context.model;
            if ((0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_1__.getMetadataComp)(notebookModel, _utils_constants__WEBPACK_IMPORTED_MODULE_2__.Selectors.notebookId, jupyterVersion)) {
                // if no instance_id yet, assign a random one
                if (!(0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_1__.getMetadataComp)(notebookModel, _utils_constants__WEBPACK_IMPORTED_MODULE_2__.Selectors.instanceId, jupyterVersion)) {
                    (0,_utils_compatibility__WEBPACK_IMPORTED_MODULE_1__.setMetadataComp)(notebookModel, _utils_constants__WEBPACK_IMPORTED_MODULE_2__.Selectors.instanceId, (0,uuid__WEBPACK_IMPORTED_MODULE_3__["default"])(), jupyterVersion);
                }
            }
        });
    }
    get isDisposed() {
        return this._isDisposed;
    }
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
    }
}


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
/* harmony import */ var _extensions_FocusExtension__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./extensions/FocusExtension */ "./lib/extensions/FocusExtension.js");
/* harmony import */ var _extensions_ExecutionExtension__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./extensions/ExecutionExtension */ "./lib/extensions/ExecutionExtension.js");
/* harmony import */ var _extensions_AlterationExtension__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./extensions/AlterationExtension */ "./lib/extensions/AlterationExtension.js");
/* harmony import */ var _extensions_InstanceInitializer__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./extensions/InstanceInitializer */ "./lib/extensions/InstanceInitializer.js");
/* harmony import */ var _extensions_CellMappingExtension__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./extensions/CellMappingExtension */ "./lib/extensions/CellMappingExtension.js");
/* harmony import */ var _utils_constants__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils/constants */ "./lib/utils/constants.js");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils_utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./utils/utils */ "./lib/utils/utils.js");








const activate = (app, settingRegistry) => {
    console.log(`JupyterLab extension ${_utils_constants__WEBPACK_IMPORTED_MODULE_1__.PLUGIN_ID} is activated!`);
    const targetVersion = '3.1.0';
    const appNumbers = app.version.match(/[0-9]+/g);
    if (appNumbers && (0,_utils_utils__WEBPACK_IMPORTED_MODULE_2__.compareVersions)(app.version, targetVersion) >= 0) {
        settingRegistry.load(`${_utils_constants__WEBPACK_IMPORTED_MODULE_1__.PLUGIN_ID}:settings`).catch((err) => {
            console.error(`${_utils_constants__WEBPACK_IMPORTED_MODULE_1__.PLUGIN_ID}: Could not load settings, error: ${err}`);
        });
        const jupyterVersion = parseInt(appNumbers[0]);
        // // adds an instance_id to the notebook
        app.docRegistry.addWidgetExtension('Notebook', new _extensions_InstanceInitializer__WEBPACK_IMPORTED_MODULE_3__.InstanceInitializer(jupyterVersion));
        // // updates the notebook metadata to track the current-to-original notebook cell id mapping
        app.docRegistry.addWidgetExtension('Notebook', new _extensions_CellMappingExtension__WEBPACK_IMPORTED_MODULE_4__.CellMappingExtension(jupyterVersion));
        const labShell = app.shell;
        // notebook widget extension with notebook ON/OFF + cell ON/OFF messaging
        app.docRegistry.addWidgetExtension('Notebook', new _extensions_FocusExtension__WEBPACK_IMPORTED_MODULE_5__.FocusExtension(labShell, settingRegistry, jupyterVersion));
        // notebook widget extension with cell insertion/deletion messaging
        app.docRegistry.addWidgetExtension('Notebook', new _extensions_AlterationExtension__WEBPACK_IMPORTED_MODULE_6__.AlterationExtension(settingRegistry, jupyterVersion));
        // notebook widget extension with code and markdown cell execution messaging
        app.docRegistry.addWidgetExtension('Notebook', new _extensions_ExecutionExtension__WEBPACK_IMPORTED_MODULE_7__.ExecutionExtension(settingRegistry, jupyterVersion));
    }
    else {
        console.log(`Use a more recent version of JupyterLab (>=${targetVersion})`);
    }
};
const plugin = {
    id: `${_utils_constants__WEBPACK_IMPORTED_MODULE_1__.PLUGIN_ID}:plugin`,
    autoStart: true,
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry],
    activate: activate
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/utils/compatibility.js":
/*!************************************!*\
  !*** ./lib/utils/compatibility.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   getCellIdsComp: () => (/* binding */ getCellIdsComp),
/* harmony export */   getMetadataComp: () => (/* binding */ getMetadataComp),
/* harmony export */   setMetadataComp: () => (/* binding */ setMetadataComp)
/* harmony export */ });
const getMetadataComp = (model, key, jupyterVersion) => {
    var _a;
    if (jupyterVersion === 4) {
        return model === null || model === void 0 ? void 0 : model.getMetadata(key);
    }
    else {
        return (_a = model === null || model === void 0 ? void 0 : model.metadata) === null || _a === void 0 ? void 0 : _a.get(key);
    }
};
const setMetadataComp = (model, key, value, jupyterVersion) => {
    var _a;
    if (jupyterVersion === 4) {
        model === null || model === void 0 ? void 0 : model.setMetadata(key, value);
    }
    else {
        (_a = model === null || model === void 0 ? void 0 : model.metadata) === null || _a === void 0 ? void 0 : _a.set(key, value);
    }
};
const getCellIdsComp = (cells, jupyterVersion) => {
    if (jupyterVersion === 4) {
        return Array.from(cells).map((item) => item.id);
    }
    else {
        return Array.from({ length: cells.length }, (_, index) => cells.get(index).id);
    }
};


/***/ }),

/***/ "./lib/utils/constants.js":
/*!********************************!*\
  !*** ./lib/utils/constants.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   BACKEND_API_URL: () => (/* binding */ BACKEND_API_URL),
/* harmony export */   MAX_PAYLOAD_SIZE: () => (/* binding */ MAX_PAYLOAD_SIZE),
/* harmony export */   PLUGIN_ID: () => (/* binding */ PLUGIN_ID),
/* harmony export */   POST_TOKEN: () => (/* binding */ POST_TOKEN),
/* harmony export */   Selectors: () => (/* binding */ Selectors)
/* harmony export */ });
const BACKEND_API_URL = 'https://api.unianalytics.ch/send/';
// export const BACKEND_API_URL = 'http://localhost:5000/send/';
const PLUGIN_ID = 'notebooksend';
const MAX_PAYLOAD_SIZE = 1048576; // 1*1024*1024 => 1Mb
const POST_TOKEN = '407b1e36627f49f28fe51d06233d9765';
// notebook metadata field names
const SELECTOR_ID = 'unianalytics';
var Selectors;
(function (Selectors) {
    Selectors.notebookId = `${SELECTOR_ID}_notebook_id`;
    Selectors.instanceId = `${SELECTOR_ID}_instance_id`;
    Selectors.cellMapping = `${SELECTOR_ID}_cell_mapping`;
})(Selectors || (Selectors = {}));


/***/ }),

/***/ "./lib/utils/utils.js":
/*!****************************!*\
  !*** ./lib/utils/utils.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   compareVersions: () => (/* binding */ compareVersions),
/* harmony export */   computeLength: () => (/* binding */ computeLength),
/* harmony export */   isNotebookValid: () => (/* binding */ isNotebookValid),
/* harmony export */   processCellOutput: () => (/* binding */ processCellOutput)
/* harmony export */ });
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./constants */ "./lib/utils/constants.js");
/* harmony import */ var _compatibility__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./compatibility */ "./lib/utils/compatibility.js");


const isNotebookValid = (panel, jupyterVersion) => {
    if (panel && !panel.isDisposed) {
        return ((0,_compatibility__WEBPACK_IMPORTED_MODULE_0__.getMetadataComp)(panel.context.model, _constants__WEBPACK_IMPORTED_MODULE_1__.Selectors.notebookId, jupyterVersion) &&
            (0,_compatibility__WEBPACK_IMPORTED_MODULE_0__.getMetadataComp)(panel.context.model, _constants__WEBPACK_IMPORTED_MODULE_1__.Selectors.instanceId, jupyterVersion) &&
            (0,_compatibility__WEBPACK_IMPORTED_MODULE_0__.getMetadataComp)(panel.context.model, _constants__WEBPACK_IMPORTED_MODULE_1__.Selectors.cellMapping, jupyterVersion));
    }
    else {
        return false;
    }
};
const compareVersions = (version1, version2) => {
    // extract numeric parts by splitting at non-digit characters
    const parts1 = version1.split(/[^0-9]+/).map(Number);
    const parts2 = version2.split(/[^0-9]+/).map(Number);
    for (let i = 0; i < Math.min(parts1.length, parts2.length); i++) {
        const num1 = parts1[i];
        const num2 = parts2[i];
        if (num1 !== num2) {
            return num1 - num2;
        }
    }
    // if all numeric parts are equal, compare the string parts
    const str1 = version1.replace(/[0-9]+/g, '');
    const str2 = version2.replace(/[0-9]+/g, '');
    return str1.localeCompare(str2);
};
// function to compute the length as a string of the content of JSON IOutput message objects as described in the Jupyterlab docs
const computeLength = (value) => {
    let totalLength = 0;
    if (typeof value === 'string') {
        totalLength = value.length;
    }
    else if (Array.isArray(value)) {
        for (const str of value) {
            totalLength += str.length;
        }
    }
    else {
        for (const key in value) {
            totalLength += JSON.stringify(value[key]).length;
        }
    }
    return totalLength;
};
const processCellOutput = (outputs) => {
    let cell_output_length = 0;
    let status = 'ok';
    for (const output of outputs) {
        const output_type = output.output_type;
        if (output_type === 'stream') {
            const multilineStr = output.text;
            cell_output_length += computeLength(multilineStr);
        }
        else if (output_type === 'error') {
            // only change status to error if an error message occurred
            status = 'error';
            cell_output_length += output.evalue.length;
        }
        else if (output_type === 'execute_result') {
            cell_output_length += computeLength(output.data);
        }
        else if (output_type === 'display_data') {
            cell_output_length += computeLength(output.data);
        }
        else {
            cell_output_length += 0;
        }
    }
    return {
        status,
        cell_output_length
    };
};


/***/ }),

/***/ "./node_modules/uuid/dist/esm-browser/regex.js":
/*!*****************************************************!*\
  !*** ./node_modules/uuid/dist/esm-browser/regex.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (/^(?:[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}|00000000-0000-0000-0000-000000000000)$/i);

/***/ }),

/***/ "./node_modules/uuid/dist/esm-browser/rng.js":
/*!***************************************************!*\
  !*** ./node_modules/uuid/dist/esm-browser/rng.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ rng)
/* harmony export */ });
// Unique ID creation requires a high quality random # generator. In the browser we therefore
// require the crypto API and do not support built-in fallback to lower quality random number
// generators (like Math.random()).
var getRandomValues;
var rnds8 = new Uint8Array(16);
function rng() {
  // lazy load so that environments that need to polyfill have a chance to do so
  if (!getRandomValues) {
    // getRandomValues needs to be invoked in a context where "this" is a Crypto implementation. Also,
    // find the complete implementation of crypto (msCrypto) on IE11.
    getRandomValues = typeof crypto !== 'undefined' && crypto.getRandomValues && crypto.getRandomValues.bind(crypto) || typeof msCrypto !== 'undefined' && typeof msCrypto.getRandomValues === 'function' && msCrypto.getRandomValues.bind(msCrypto);

    if (!getRandomValues) {
      throw new Error('crypto.getRandomValues() not supported. See https://github.com/uuidjs/uuid#getrandomvalues-not-supported');
    }
  }

  return getRandomValues(rnds8);
}

/***/ }),

/***/ "./node_modules/uuid/dist/esm-browser/stringify.js":
/*!*********************************************************!*\
  !*** ./node_modules/uuid/dist/esm-browser/stringify.js ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _validate_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./validate.js */ "./node_modules/uuid/dist/esm-browser/validate.js");

/**
 * Convert array of 16 byte values to UUID string format of the form:
 * XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
 */

var byteToHex = [];

for (var i = 0; i < 256; ++i) {
  byteToHex.push((i + 0x100).toString(16).substr(1));
}

function stringify(arr) {
  var offset = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 0;
  // Note: Be careful editing this code!  It's been tuned for performance
  // and works in ways you may not expect. See https://github.com/uuidjs/uuid/pull/434
  var uuid = (byteToHex[arr[offset + 0]] + byteToHex[arr[offset + 1]] + byteToHex[arr[offset + 2]] + byteToHex[arr[offset + 3]] + '-' + byteToHex[arr[offset + 4]] + byteToHex[arr[offset + 5]] + '-' + byteToHex[arr[offset + 6]] + byteToHex[arr[offset + 7]] + '-' + byteToHex[arr[offset + 8]] + byteToHex[arr[offset + 9]] + '-' + byteToHex[arr[offset + 10]] + byteToHex[arr[offset + 11]] + byteToHex[arr[offset + 12]] + byteToHex[arr[offset + 13]] + byteToHex[arr[offset + 14]] + byteToHex[arr[offset + 15]]).toLowerCase(); // Consistency check for valid UUID.  If this throws, it's likely due to one
  // of the following:
  // - One or more input array values don't map to a hex octet (leading to
  // "undefined" in the uuid)
  // - Invalid input values for the RFC `version` or `variant` fields

  if (!(0,_validate_js__WEBPACK_IMPORTED_MODULE_0__["default"])(uuid)) {
    throw TypeError('Stringified UUID is invalid');
  }

  return uuid;
}

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (stringify);

/***/ }),

/***/ "./node_modules/uuid/dist/esm-browser/v4.js":
/*!**************************************************!*\
  !*** ./node_modules/uuid/dist/esm-browser/v4.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _rng_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./rng.js */ "./node_modules/uuid/dist/esm-browser/rng.js");
/* harmony import */ var _stringify_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./stringify.js */ "./node_modules/uuid/dist/esm-browser/stringify.js");



function v4(options, buf, offset) {
  options = options || {};
  var rnds = options.random || (options.rng || _rng_js__WEBPACK_IMPORTED_MODULE_0__["default"])(); // Per 4.4, set bits for version and `clock_seq_hi_and_reserved`

  rnds[6] = rnds[6] & 0x0f | 0x40;
  rnds[8] = rnds[8] & 0x3f | 0x80; // Copy bytes to buffer, if provided

  if (buf) {
    offset = offset || 0;

    for (var i = 0; i < 16; ++i) {
      buf[offset + i] = rnds[i];
    }

    return buf;
  }

  return (0,_stringify_js__WEBPACK_IMPORTED_MODULE_1__["default"])(rnds);
}

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (v4);

/***/ }),

/***/ "./node_modules/uuid/dist/esm-browser/validate.js":
/*!********************************************************!*\
  !*** ./node_modules/uuid/dist/esm-browser/validate.js ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _regex_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./regex.js */ "./node_modules/uuid/dist/esm-browser/regex.js");


function validate(uuid) {
  return typeof uuid === 'string' && _regex_js__WEBPACK_IMPORTED_MODULE_0__["default"].test(uuid);
}

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (validate);

/***/ })

}]);
//# sourceMappingURL=lib_index_js.5e45435c16a06ddad607.js.map