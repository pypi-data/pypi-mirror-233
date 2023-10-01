/*
 * for attaching keybindings later on, see
 * https://towardsdatascience.com/how-to-customize-jupyterlab-keyboard-shortcuts-72321f73753d
 */

/* eslint-disable prettier/prettier */

import { JupyterFrontEnd, JupyterFrontEndPlugin, } from '@jupyterlab/application'
import { ICommandPalette } from '@jupyterlab/apputils'
import { INotebookTracker, NotebookPanel, INotebookModel } from '@jupyterlab/notebook'
import { Cell } from '@jupyterlab/cells'

import { IDisposable, DisposableDelegate } from '@lumino/disposable'
import { DocumentRegistry } from '@jupyterlab/docregistry'
import { ToolbarButton } from '@jupyterlab/apputils'

import { md_get, md_unset, md_has, md_insert, md_remove, md_toggle } from 'jupyterlab-celltagsclasses'
import { Scope, apply_on_cells } from 'jupyterlab-celltagsclasses'

import { toggle_admonition } from './admonitions'

// md_clean may be broken
// import { md_set, , md_insert, md_remove } from 'jupyterlab-celltagsclasses'


const clean_cell_metadata = (cell: Cell) => {
  console.log("Cleaning metadata for cell", cell)
  const editable = cell.model.getMetadata('editable')
  if (editable === true) {
    md_unset(cell, 'editable')
  }
  const tags = cell.model.getMetadata('tags')
  if (tags?.length === 0) {
    md_unset(cell, 'tags')
  }
  const slide_type = md_get(cell, 'slideshow.slide_type')
  if (slide_type === '') {
    md_unset(cell, 'slideshow.slide_type')
  }
  const slideshow = md_get(cell, 'slideshow')
  if ((slideshow !== undefined) && (JSON.stringify(slideshow) == '{}')) {
    md_unset(cell, 'slideshow')
  }
  const user_expressions = md_get(cell, 'user_expressions')
  if (user_expressions?.length === 0) {
    md_unset(cell, 'user_expressions')
  }
}



const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-courselevels:plugin',
  autoStart: true,
  requires: [ICommandPalette, INotebookTracker],
  activate: (app: JupyterFrontEnd, palette: ICommandPalette, notebookTracker: INotebookTracker) => {
    console.log('extension jupyterlab-courselevels is activating')
    // https://lumino.readthedocs.io/en/1.x/api/commands/interfaces/commandregistry.ikeybindingoptions.html
    // The supported modifiers are: Accel, Alt, Cmd, Ctrl, and Shift. The Accel
    // modifier is translated to Cmd on Mac and Ctrl on all other platforms. The
    // Cmd modifier is ignored on non-Mac platforms.
    // Alt is option on mac

    const cell_toggle_level = (cell: Cell, level: string): void => {
      switch (level) {
        case 'basic':
          if (md_has(cell, 'tags', 'level_basic')) {
            md_remove(cell, 'tags', 'level_basic')
          } else {
            md_insert(cell, 'tags', 'level_basic')
            md_remove(cell, 'tags', 'level_intermediate')
            md_remove(cell, 'tags', 'level_advanced')
          }
          break
        case 'intermediate':
          if (md_has(cell, 'tags', 'level_intermediate')) {
            md_remove(cell, 'tags', 'level_intermediate')
          } else {
            md_remove(cell, 'tags', 'level_basic')
            md_insert(cell, 'tags', 'level_intermediate')
            md_remove(cell, 'tags', 'level_advanced')
          }
          break
        case 'advanced':
          if (md_has(cell, 'tags', 'level_advanced')) {
            md_remove(cell, 'tags', 'level_advanced')
          } else {
            md_remove(cell, 'tags', 'level_basic')
            md_remove(cell, 'tags', 'level_intermediate')
            md_insert(cell, 'tags', 'level_advanced')
          }
          break
        default:
          md_remove(cell, 'tags', 'level_basic')
          md_remove(cell, 'tags', 'level_intermediate')
          md_remove(cell, 'tags', 'level_advanced')
      }
    }

    const toggle_level = (level: string) => {
      apply_on_cells(notebookTracker, Scope.Active, (cell: Cell) => {
        cell_toggle_level(cell, level)
      })
    }

    let command

    for (const [level, key] of [
      ['basic', 'Ctrl X'],
      ['intermediate', 'Ctrl Y'],
      ['advanced', 'Ctrl Z'],
    ]) {
      command = `courselevels:toggle-level-${level}`
      app.commands.addCommand(command, {
        label: `toggle ${level} level`,
        execute: () => toggle_level(level)
      })
      palette.addItem({ command, category: 'CourseLevels' })
      app.commands.addKeyBinding({ command, keys: ['Ctrl \\', key], selector: '.jp-Notebook' })
    }


    const toggle_frame = () => {
      apply_on_cells(notebookTracker, Scope.Active, (cell: Cell) => {
        md_toggle(cell, 'tags', 'framed_cell')
      })
    }

    command = 'courselevels:toggle-frame'
    app.commands.addCommand(command, {
      label: 'toggle frame',
      execute: () => toggle_frame()
    })
    palette.addItem({ command, category: 'CourseLevels' })
    app.commands.addKeyBinding({ command, keys: ['Ctrl \\', 'Ctrl M'], selector: '.jp-Notebook' })



    const toggle_licence = () => {
      apply_on_cells(notebookTracker, Scope.Active, (cell: Cell) => {
        md_toggle(cell, 'tags', 'licence')
      })
    }

    command = 'courselevels:toggle-licence'
    app.commands.addCommand(command, {
      label: 'toggle licence',
      execute: () => toggle_licence()
    })
    palette.addItem({ command, category: 'CourseLevels' })
    app.commands.addKeyBinding({ command, keys: ['Ctrl \\', 'Ctrl L'], selector: '.jp-Notebook' })


    command = 'courselevels:metadata-clean-selected'
    app.commands.addCommand(command, {
      label: `clean metadata for all selected cells`,
      execute: () => apply_on_cells(notebookTracker, Scope.Multiple, clean_cell_metadata)
    })
    palette.addItem({ command, category: 'courselevels' })
    app.commands.addKeyBinding({ command, keys: ['Alt Cmd 7'], selector: '.jp-Notebook' })


    command = 'courselevels:metadata-clean-all'
    app.commands.addCommand(command, {
      label: `clean metadata for all cells`,
      execute: () => apply_on_cells(notebookTracker, Scope.All, clean_cell_metadata)
    })
    palette.addItem({ command, category: 'courselevels' })
    app.commands.addKeyBinding({ command, keys: ['Ctrl Alt 7'], selector: '.jp-Notebook' })


// the buttons in the toolbar

    const find_spacer = (panel: NotebookPanel): number => {
      let index = 0
      for (const child of panel.toolbar.children()) {
        if (child.node.classList.contains('jp-Toolbar-spacer')) {
          return index
        } else {
          index += 1
        }
      }
      return 0
    }

    class BasicButton implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
      createNew(panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable {
        const button = new ToolbarButton({
          className: 'courselevels-button',
          iconClass: 'far fa-hand-pointer',
          onClick: () => toggle_level('basic'),
          tooltip: 'Toggle basic level',
        })
        // compute where to insert it
        const index = find_spacer(panel)
        panel.toolbar.insertItem(index, 'basicLevel', button)
        return new DisposableDelegate(() => {
          button.dispose()
        })
      }
    }
    app.docRegistry.addWidgetExtension('Notebook', new BasicButton())

    class IntermediateButton implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
      createNew(panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable {
        const button = new ToolbarButton({
          className: 'courselevels-button',
          iconClass: 'far fa-hand-peace',
          onClick: () => toggle_level('intermediate'),
          tooltip: 'Toggle intermediate level',
        })
        // compute where to insert it
        const index = find_spacer(panel)
        panel.toolbar.insertItem(index, 'intermediateLevel', button)
        return new DisposableDelegate(() => {
          button.dispose()
        })
      }
    }
    app.docRegistry.addWidgetExtension('Notebook', new IntermediateButton())

    class AdvancedButton implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
      createNew(panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable {
        const button = new ToolbarButton({
          className: 'courselevels-button',
          iconClass: 'far fa-hand-spock',
          onClick: () => toggle_level('advanced'),
          tooltip: 'Toggle advanced level',
        })
        // compute where to insert it
        const index = find_spacer(panel)
        panel.toolbar.insertItem(index, 'advancedLevel', button)
        return new DisposableDelegate(() => {
          button.dispose()
        })
      }
    }
    app.docRegistry.addWidgetExtension('Notebook', new AdvancedButton())

    class FrameButton implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
      createNew(panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable {
        const button = new ToolbarButton({
          className: 'courselevels-button',
          iconClass: 'fas fa-crop-alt',
          onClick: () => toggle_frame(),
          tooltip: 'Toggle frame around cell',
        })
        // compute where to insert it
        const index = find_spacer(panel)
        panel.toolbar.insertItem(index, 'frameLevel', button)
        return new DisposableDelegate(() => {
          button.dispose()
        })
      }
    }
    app.docRegistry.addWidgetExtension('Notebook', new FrameButton())

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
      const admonition = name as string
      command = 'courselevels:toggle-admonition'
      let label = 'toggle admonition'
      if (admonition !== 'admonition') {
        command += `-${admonition}`
        label += ` ${admonition}`
      }
      app.commands.addCommand(command, {
        label,
        execute: () => {
          const notebook = notebookTracker.currentWidget?.content
          if (notebook === undefined) { return }
          toggle_admonition(notebook, admonition)
        }
      })
      palette.addItem({ command, category: 'CourseLevels' })
      if (key !== null) {
        app.commands.addKeyBinding({ command, keys: ['Ctrl \\', key], selector: '.jp-Notebook' })
      }
    }
  }

}

export default plugin
