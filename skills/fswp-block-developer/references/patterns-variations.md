# Patterns, variations, hooks, and bindings

## Choosing the right extension point

| Goal | Use |
|---|---|
| Reusable arrangement of existing blocks with starter text | **Pattern** |
| Same block, different starting attributes or inner blocks | **Block variation** |
| Alternative visual look of an existing block | **Block style** |
| Insert a block automatically near another block type | **Block hooks** (`blockHooks` in block.json, WordPress 6.4+) |
| Show data from post meta or another source inside a core block attribute | **Block Bindings API** (`register_block_bindings_source`); confirm the minimum WordPress version and which core blocks and attributes are bindable |
| New behavior that no core block can express | **Custom block** |

## Patterns

- Plugin: `register_block_pattern_category( 'slug', array( 'label' => __( 'Label', 'domain' ) ) )` then `register_block_pattern( 'vendor/name', array( 'title' => ..., 'categories' => array( 'slug' ), 'content' => '<!-- wp:group -->...' ) )`, both on `init`.
- Theme: one PHP file per pattern in `patterns/` with a header comment (Title, Slug, Categories, Keywords, Viewport Width, Block Types, Inserter). The file's output is the pattern content.
- Use theme presets (`var(--wp--preset--color--primary)`), not hard-coded colors; translate visible text; no remote images; keep block markup valid (correct comment delimiters and closing tags).
- Post-type or template-specific patterns use the `Block Types` / `templateTypes` header fields.

## Variations and styles

- Variations: `variations` in block.json or `registerBlockVariation()`; set `isActive` so the editor shows which variation is selected.
- Styles: `styles` in block.json, `register_block_style()` in PHP, or style variations in theme.json for whole-site looks.

## Testing

Insert each pattern in the editor, switch to code view to confirm there is no block validation error, and check the front end and a narrow viewport.
