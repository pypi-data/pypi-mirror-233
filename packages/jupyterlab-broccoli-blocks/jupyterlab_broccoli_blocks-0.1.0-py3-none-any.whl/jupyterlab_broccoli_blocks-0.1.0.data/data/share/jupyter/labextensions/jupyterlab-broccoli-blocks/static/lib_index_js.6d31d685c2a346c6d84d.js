(self["webpackChunkjupyterlab_broccoli_blocks"] = self["webpackChunkjupyterlab_broccoli_blocks"] || []).push([["lib_index_js"],{

/***/ "./lib/blocks.js":
/*!***********************!*\
  !*** ./lib/blocks.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TOOLBOX": () => (/* binding */ TOOLBOX)
/* harmony export */ });
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! blockly */ "webpack/sharing/consume/default/blockly/blockly");
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(blockly__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _toolbox_special__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./toolbox_special */ "./lib/toolbox_special.js");

//import { ToolboxUtils } from './utils';
//import { TOOLBOX_BASIC } from './toolbox_basic';

//
//const toolboxUtils = new ToolboxUtils();
//export const TOOLBOX = toolboxUtils.add(TOOLBOX_BASIC, TOOLBOX_SPECIAL, 1);
const TOOLBOX = _toolbox_special__WEBPACK_IMPORTED_MODULE_1__.TOOLBOX_SPECIAL;
// text_nocrlf_print
blockly__WEBPACK_IMPORTED_MODULE_0__.defineBlocksWithJsonArray([{
        'type': 'text_nocrlf_print',
        'message0': '%{BKY_BLOCK_TEXT_NOCRLF_PRINT}  %1',
        'args0': [
            {
                'type': 'input_value',
                'name': 'TEXT',
                'check': 'String',
            }
        ],
        'inputsInline': false,
        'previousStatement': null,
        'nextStatement': null,
        'colour': 230,
        'tooltip': '',
        'helpUrl': ''
    }]);
// color_hsv2rgb
blockly__WEBPACK_IMPORTED_MODULE_0__.defineBlocksWithJsonArray([{
        'type': 'color_hsv2rgb',
        'message0': '%{BKY_BLOCK_COLOR_HSV2RGB}  %{BKY_BLOCK_COLOR_H}  %1 %{BKY_BLOCK_COLOR_S}  %2 %{BKY_BLOCK_COLOR_V}  %3',
        'args0': [
            {
                'type': 'input_value',
                'name': 'H',
                'check': 'Number',
                'align': 'RIGHT'
            },
            {
                'type': 'input_value',
                'name': 'S',
                'check': 'Number',
                'align': 'RIGHT'
            },
            {
                'type': 'input_value',
                'name': 'V',
                'check': 'Number',
                'align': 'RIGHT'
            },
        ],
        'output': 'Colour',
        'colour': 230,
        'helpUrl': '',
        'tooltip': '',
    }]);


/***/ }),

/***/ "./lib/dart/func.js":
/*!**************************!*\
  !*** ./lib/dart/func.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "dummy_function": () => (/* binding */ dummy_function)
/* harmony export */ });
//import { dartGenerator as BlocklyGene } from 'blockly/dart';
const notImplementedMsg = 'Not implemented';
function dummy_function(block, generator) {
    return notImplementedMsg;
}
;


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var jupyterlab_broccoli__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jupyterlab-broccoli */ "webpack/sharing/consume/default/jupyterlab-broccoli/jupyterlab-broccoli");
/* harmony import */ var jupyterlab_broccoli__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jupyterlab_broccoli__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _blocks__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./blocks */ "./lib/blocks.js");
/* harmony import */ var _python_func_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./python/func.js */ "./lib/python/func.js");
/* harmony import */ var _javascript_func_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./javascript/func.js */ "./lib/javascript/func.js");
/* harmony import */ var _lua_func_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./lua/func.js */ "./lib/lua/func.js");
/* harmony import */ var _dart_func_js__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./dart/func.js */ "./lib/dart/func.js");
/* harmony import */ var _php_func_js__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./php/func.js */ "./lib/php/func.js");








/**
 * Initialization data for the jupyterlab-broccoli-blocks extension.
 */
const plugin = {
    id: 'jupyterlab-broccoli-blocks:plugin',
    autoStart: true,
    requires: [jupyterlab_broccoli__WEBPACK_IMPORTED_MODULE_0__.IBlocklyRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.ITranslator],
    activate: (app, register, translator) => {
        console.log('JupyterLab extension jupyterlab-broccoli-blocks is activated!');
        // Localization 
        const language = register.language;
        __webpack_require__("./lib/msg lazy recursive ^\\.\\/.*\\.js$")(`./${language}.js`)
            .catch(() => {
            if (language !== 'En') {
                __webpack_require__.e(/*! import() */ "lib_msg_En_js").then(__webpack_require__.bind(__webpack_require__, /*! ./msg/En.js */ "./lib/msg/En.js"))
                    .catch(() => { });
            }
        });
        const trans = (translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator).load('jupyterlab');
        register.registerToolbox(trans.__('special'), _blocks__WEBPACK_IMPORTED_MODULE_2__.TOOLBOX);
        //
        register.registerCodes('python', _python_func_js__WEBPACK_IMPORTED_MODULE_3__);
        register.registerCodes('javascript', _javascript_func_js__WEBPACK_IMPORTED_MODULE_4__);
        register.registerCodes('lua', _lua_func_js__WEBPACK_IMPORTED_MODULE_5__);
        register.registerCodes('dart', _dart_func_js__WEBPACK_IMPORTED_MODULE_6__);
        register.registerCodes('php', _php_func_js__WEBPACK_IMPORTED_MODULE_7__);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/javascript/func.js":
/*!********************************!*\
  !*** ./lib/javascript/func.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "text_nocrlf_print": () => (/* binding */ text_nocrlf_print),
/* harmony export */   "text_print": () => (/* binding */ text_print)
/* harmony export */ });
/* harmony import */ var blockly_javascript__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! blockly/javascript */ "../../node_modules/blockly/javascript.js");
/* harmony import */ var blockly_javascript__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(blockly_javascript__WEBPACK_IMPORTED_MODULE_0__);

const Order = {
    ATOMIC: 0,
    NEW: 1.1,
    MEMBER: 1.2,
    FUNCTION_CALL: 2,
    INCREMENT: 3,
    DECREMENT: 3,
    BITWISE_NOT: 4.1,
    UNARY_PLUS: 4.2,
    UNARY_NEGATION: 4.3,
    LOGICAL_NOT: 4.4,
    TYPEOF: 4.5,
    VOID: 4.6,
    DELETE: 4.7,
    AWAIT: 4.8,
    EXPONENTIATION: 5.0,
    MULTIPLICATION: 5.1,
    DIVISION: 5.2,
    MODULUS: 5.3,
    SUBTRACTION: 6.1,
    ADDITION: 6.2,
    BITWISE_SHIFT: 7,
    RELATIONAL: 8,
    IN: 8,
    INSTANCEOF: 8,
    EQUALITY: 9,
    BITWISE_AND: 10,
    BITWISE_XOR: 11,
    BITWISE_OR: 12,
    LOGICAL_AND: 13,
    LOGICAL_OR: 14,
    CONDITIONAL: 15,
    ASSIGNMENT: 16,
    YIELD: 17,
    COMMA: 18,
    NONE: 99, // (...)
};
const notImplementedMsg = 'Not implemented at this Kernel';
function text_print(block) {
    const msg = blockly_javascript__WEBPACK_IMPORTED_MODULE_0__.javascriptGenerator.valueToCode(block, 'TEXT', Order.NONE) || "''";
    return 'console.log(' + msg + ');\n';
}
;
function text_nocrlf_print(block) {
    const msg = blockly_javascript__WEBPACK_IMPORTED_MODULE_0__.javascriptGenerator.valueToCode(block, 'TEXT', Order.NONE) || "''";
    return 'process.stdout.write(' + msg + ');\n';
}
;


/***/ }),

/***/ "./lib/lua/func.js":
/*!*************************!*\
  !*** ./lib/lua/func.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "dummy_function": () => (/* binding */ dummy_function)
/* harmony export */ });
//import { luaGenerator as BlocklyGene } from 'blockly/lua';
const notImplementedMsg = 'Not implemented';
function dummy_function(block, generator) {
    return notImplementedMsg;
}
;


/***/ }),

/***/ "./lib/php/func.js":
/*!*************************!*\
  !*** ./lib/php/func.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "dummy_function": () => (/* binding */ dummy_function)
/* harmony export */ });
//import { phpGenerator as BlocklyGene } from 'blockly/php';
const notImplementedMsg = 'Not implemented';
function dummy_function(block, generator) {
    return notImplementedMsg;
}
;


/***/ }),

/***/ "./lib/python/func.js":
/*!****************************!*\
  !*** ./lib/python/func.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "color_hsv2rgb": () => (/* binding */ color_hsv2rgb),
/* harmony export */   "text_nocrlf_print": () => (/* binding */ text_nocrlf_print)
/* harmony export */ });
/* harmony import */ var blockly_python__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! blockly/python */ "../../node_modules/blockly/python.js");
/* harmony import */ var blockly_python__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(blockly_python__WEBPACK_IMPORTED_MODULE_0__);

const Order = {
    ATOMIC: 0,
    COLLECTION: 1,
    STRING_CONVERSION: 1,
    MEMBER: 2.1,
    FUNCTION_CALL: 2.2,
    EXPONENTIATION: 3,
    UNARY_SIGN: 4,
    BITWISE_NOT: 4,
    MULTIPLICATIVE: 5,
    ADDITIVE: 6,
    BITWISE_SHIFT: 7,
    BITWISE_AND: 8,
    BITWISE_XOR: 9,
    BITWISE_OR: 10,
    RELATIONAL: 11,
    LOGICAL_NOT: 12,
    LOGICAL_AND: 13,
    LOGICAL_OR: 14,
    CONDITIONAL: 15,
    LAMBDA: 16,
    NONE: 99, // (...)
};
/**/
//
//const notImplementedMsg = 'Not implemented at this Kernel';
function text_nocrlf_print(block) {
    const msg = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'TEXT', Order.NONE) || "''";
    return 'print(' + msg + ', end="")\n';
}
;
//
function color_hsv2rgb(block) {
    let hh = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'H', Order.NONE) || "''";
    let ss = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'S', Order.NONE) || "''";
    let vv = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'V', Order.NONE) || "''";
    hh = hh % 360;
    if (hh < 0.0)
        hh = hh + 360;
    if (ss < 0.0)
        ss = 0.0;
    else if (ss > 1.0)
        ss = 1.0;
    if (vv < 0.0)
        vv = 0.0;
    else if (vv > 1.0)
        vv = 1.0;
    let aa = vv;
    let bb = vv - vv * ss;
    let rc = 0;
    let gc = 0;
    let bc = 0;
    //
    if (hh >= 0 && hh < 60) {
        rc = aa;
        gc = (hh / 60) * (aa - bb) + bb;
        bc = bb;
    }
    else if (hh >= 60 && hh < 120) {
        rc = (120 - hh) / 60 * (aa - bb) + bb;
        gc = aa;
        bc = bb;
    }
    else if (hh >= 120 && hh < 180) {
        rc = bb;
        gc = aa;
        bc = (hh - 120) / 60 * (aa - bb) + bb;
    }
    else if (hh >= 180 && hh < 240) {
        rc = bb;
        gc = (240 - hh) / 60 * (aa - bb) + bb;
        bc = aa;
    }
    else if (hh >= 240 && hh < 300) {
        rc = (hh - 240) / 60 * (aa - bb) + bb;
        gc = bb;
        bc = aa;
    }
    else { // hh>=300 and hh<360
        rc = aa;
        gc = bb;
        bc = (360 - hh) / 50 * (aa - bb) + bb;
    }
    //
    rc = Math.trunc(rc * 255);
    gc = Math.trunc(gc * 255);
    bc = Math.trunc(bc * 255);
    //
    const rgb = '#' + rc.toString(16) + gc.toString(16) + bc.toString(16);
    const code = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.quote_(rgb);
    return [code, Order.FUNCTION_CALL];
}
;
/**/


/***/ }),

/***/ "./lib/toolbox_special.js":
/*!********************************!*\
  !*** ./lib/toolbox_special.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TOOLBOX_SPECIAL": () => (/* binding */ TOOLBOX_SPECIAL)
/* harmony export */ });
const TOOLBOX_SPECIAL = {
    kind: 'categoryToolbox',
    contents: [
        {
            kind: 'CATEGORY',
            name: '%{BKY_TOOLBOX_SPECIAL}',
            colour: 330,
            contents: [
                {
                    kind: 'BLOCK',
                    type: 'text_nocrlf_print',
                    blockxml: `<block type='text_nocrlf_print'>
              <value name='TEXT'>
                <shadow type='text'>
                  <field name='TEXT'>abc</field>
                </shadow>
              </value>
            </block>`,
                },
                {
                    kind: 'BLOCK',
                    type: 'color_hsv2rgb',
                    blockxml: `<block type='color_hsv2rgb'>
              <value name='H'>
                <shadow type='math_number'>
                  <field name='NUM'>0.0</field>
                </shadow>
              </value>
              <value name='S'>
                <shadow type='math_number'>
                  <field name='NUM'>0.45</field>
                </shadow>
              </value>
              <value name='V'>
                <shadow type='math_number'>
                  <field name='NUM'>0.65</field>
                </shadow>
              </value>
            </block>`,
                },
            ]
        }
    ]
};


/***/ }),

/***/ "./lib/msg lazy recursive ^\\.\\/.*\\.js$":
/*!*****************************************************!*\
  !*** ./lib/msg/ lazy ^\.\/.*\.js$ namespace object ***!
  \*****************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var map = {
	"./En.js": [
		"./lib/msg/En.js",
		"lib_msg_En_js"
	],
	"./Jp.js": [
		"./lib/msg/Jp.js",
		"lib_msg_Jp_js"
	]
};
function webpackAsyncContext(req) {
	if(!__webpack_require__.o(map, req)) {
		return Promise.resolve().then(() => {
			var e = new Error("Cannot find module '" + req + "'");
			e.code = 'MODULE_NOT_FOUND';
			throw e;
		});
	}

	var ids = map[req], id = ids[0];
	return __webpack_require__.e(ids[1]).then(() => {
		return __webpack_require__(id);
	});
}
webpackAsyncContext.keys = () => (Object.keys(map));
webpackAsyncContext.id = "./lib/msg lazy recursive ^\\.\\/.*\\.js$";
module.exports = webpackAsyncContext;

/***/ })

}]);
//# sourceMappingURL=lib_index_js.6d31d685c2a346c6d84d.js.map