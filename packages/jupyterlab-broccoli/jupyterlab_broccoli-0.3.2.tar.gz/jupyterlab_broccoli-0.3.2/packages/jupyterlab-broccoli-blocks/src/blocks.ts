
import * as Blockly from 'blockly';

//import { ToolboxUtils } from './utils';
//import { TOOLBOX_BASIC } from './toolbox_basic';
import { TOOLBOX_SPECIAL } from './toolbox_special';

//
//const toolboxUtils = new ToolboxUtils();
//export const TOOLBOX = toolboxUtils.add(TOOLBOX_BASIC, TOOLBOX_SPECIAL, 1);
export const TOOLBOX = TOOLBOX_SPECIAL;

// text_nocrlf_print
Blockly.defineBlocksWithJsonArray(
[{
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
Blockly.defineBlocksWithJsonArray(
[{
  'type': 'color_hsv2rgb',
  'message0': 
    '%{BKY_BLOCK_COLOR_HSV2RGB}  %{BKY_BLOCK_COLOR_H}  %1 %{BKY_BLOCK_COLOR_S}  %2 %{BKY_BLOCK_COLOR_V}  %3',
  'args0': [
    {
      'type':  'input_value',
      'name':  'H',
      'check': 'Number',
      'align': 'RIGHT'
    },
    {
      'type':  'input_value',
      'name':  'S',
      'check': 'Number',
      'align': 'RIGHT'
    },
    {
      'type':  'input_value',
      'name':  'V',
      'check': 'Number',
      'align': 'RIGHT'
    },
  ],
  'output': 'Colour',
  'colour': 230,
  'helpUrl': '',
  'tooltip': '',
}]);

