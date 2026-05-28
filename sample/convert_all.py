import os
import re

spec_dir = "/Users/jasonfox/Workspace/dita/dita-ot-4.2/plugins/dita-bootstrap.specialization/sample"
base_dir = "/Users/jasonfox/Workspace/dita/dita-ot-4.2/plugins/dita-bootstrap/sample"

spec_files = [f for f in os.listdir(spec_dir) if f.endswith('.dita')]

def transform_tag(tag_name, attrs, self_closing):
    attr_dict = {}
    if attrs:
        # Match attributes like name="value" or xml:name="value"
        for m in re.finditer(r'([a-zA-Z0-9_-]+|xml:[a-zA-Z0-9_-]+)="([^"]*)"', attrs):
            attr_dict[m.group(1)] = m.group(2)
            
    target_tag = tag_name
    outputclass_parts = []
    otherprops_parts = []
    
    # Custom mapping of specialized tags
    if tag_name == 'tabbed-dialog':
        target_tag = 'bodydiv'
        style = attr_dict.pop('style', 'tabs')
        if style == 'pills':
            outputclass_parts.append('nav-pills')
        elif style == 'vertical-pills':
            outputclass_parts.append('nav-pills-vertical')
        else:
            outputclass_parts.append('nav-tabs')
            
    elif tag_name == 'accordion':
        target_tag = 'bodydiv'
        flush = attr_dict.pop('flush', 'no')
        open_val = attr_dict.pop('open', 'no')
        if flush == 'yes':
            outputclass_parts.append('accordion-flush')
        elif open_val == 'yes':
            outputclass_parts.append('accordion-open')
        else:
            outputclass_parts.append('accordion')
            
    elif tag_name == 'accordion-item':
        target_tag = 'section'
        open_val = attr_dict.pop('open', 'no')
        if open_val == 'yes':
            outputclass_parts.append('show')
            
    elif tag_name == 'alert':
        target_tag = 'section'
        outputclass_parts.append('alert')
        color = attr_dict.pop('color', '')
        if color:
            outputclass_parts.append(f'alert-{color}')
            
    elif tag_name == 'badge':
        target_tag = 'ph'
        outputclass_parts.append('badge')
        color = attr_dict.pop('color', 'primary')
        outputclass_parts.append(f'text-bg-{color}')
        
    elif tag_name == 'button':
        target_tag = 'xref'
        color = attr_dict.pop('color', 'primary')
        outline = attr_dict.pop('outline', 'no')
        size = attr_dict.pop('size', '')
        
        btn_class = 'btn'
        if outline == 'yes':
            btn_class += f'-outline-{color}'
        else:
            btn_class += f'-{color}'
            
        outputclass_parts.append(btn_class)
        if size == 'large':
            outputclass_parts.append('btn-lg')
        elif size == 'small':
            outputclass_parts.append('btn-sm')
            
    elif tag_name == 'button-group':
        target_tag = 'bodydiv'
        vertical = attr_dict.pop('vertical', 'no')
        if vertical == 'yes':
            outputclass_parts.append('btn-group-vertical')
        else:
            outputclass_parts.append('btn-group')
            
    elif tag_name == 'button-toolbar':
        target_tag = 'bodydiv'
        outputclass_parts.append('btn-toolbar')
        
    elif tag_name == 'card':
        target_tag = 'section'
        outputclass_parts.append('card')
        color = attr_dict.pop('color', '')
        if color:
            outputclass_parts.append(f'text-bg-{color}')
            
    elif tag_name == 'card-header':
        target_tag = 'div'
        outputclass_parts.append('card-header')
        
    elif tag_name == 'card-footer':
        target_tag = 'div'
        outputclass_parts.append('card-footer')
        
    elif tag_name == 'carousel':
        target_tag = 'ol'
        outputclass_parts.append('carousel')
        indicators = attr_dict.pop('indicators', 'no')
        interval = attr_dict.pop('interval', '')
        touch = attr_dict.pop('touch', '')
        autoplay = attr_dict.pop('autoplay', '')
        fade = attr_dict.pop('fade', 'no')
        
        if fade == 'yes':
            outputclass_parts = ['carousel-fade']
            
        if indicators == 'yes':
            otherprops_parts.append('indicators(true)')
        if autoplay == 'no':
            otherprops_parts.append('autoplay(false)')
        if touch == 'no':
            otherprops_parts.append('touch(false)')
            
    elif tag_name == 'carousel-item':
        target_tag = 'li'
        # Move interval attribute to otherprops (not valid on li in standard DTD)
        interval = attr_dict.pop('interval', '')
        if interval:
            otherprops_parts.append(f'interval({interval})')
        
    elif tag_name == 'collapse':
        target_tag = 'bodydiv'
        outputclass_parts.append('collapse')
        
    elif tag_name == 'icon':
        target_tag = 'ph'
        op = attr_dict.get('outputclass', '')
        if op:
            if op.startswith('bi-'):
                attr_dict['outputclass'] = f'bi {op}'
            elif not op.startswith('bi '):
                attr_dict['outputclass'] = f'bi bi-{op}'
        else:
            outputclass_parts.append('bi')
            
    elif tag_name == 'grid-row':
        target_tag = 'bodydiv'  # bodydiv allows block-level children like section
        outputclass_parts.append('row')
        
    elif tag_name == 'grid-col':
        target_tag = 'bodydiv'  # bodydiv allows block-level children like section
        breakpoint = attr_dict.pop('breakpoint', '')
        colspan = attr_dict.pop('colspan', '')
        col_class = 'col'
        if breakpoint and colspan:
            col_class = f'col-{breakpoint}-{colspan}'
        elif colspan:
            col_class = f'col-{colspan}'
        elif breakpoint:
            col_class = f'col-{breakpoint}'
        outputclass_parts.append(col_class)
        
    elif tag_name == 'list-group':
        target_tag = 'ul'
        outputclass_parts.append('list-group')
        flush = attr_dict.pop('flush', 'no')
        compact = attr_dict.pop('compact', 'no')
        if flush == 'yes':
            outputclass_parts.append('list-group-flush')
        if compact == 'yes':
            outputclass_parts.append('list-group-compact')
            
        color = attr_dict.pop('color', '')
        if color:
            outputclass_parts.append(f'list-group-item-{color}')
            
    elif tag_name == 'offcanvas':
        target_tag = 'section'
        outputclass_parts.append('offcanvas')
        pos = attr_dict.pop('position', 'start')
        outputclass_parts.append(f'offcanvas-{pos}')
        
    elif tag_name == 'pagination':
        target_tag = 'section'
        outputclass_parts.append('pagination')
        size = attr_dict.pop('size', '')
        if size == 'large':
            outputclass_parts.append('pagination-lg')
        elif size == 'small':
            outputclass_parts.append('pagination-sm')
            
    elif tag_name == 'popover':
        target_tag = 'xref'
        pos = attr_dict.pop('position', 'top')
        outputclass_parts.append(f'popover-{pos}')
        
    elif tag_name == 'thumbnail':
        target_tag = 'image'
        outputclass_parts.append('img-thumbnail')
        color = attr_dict.pop('color', '')
        if color:
            outputclass_parts.append(f'bg-{color}')
            
    elif tag_name == 'tooltip':
        target_tag = 'xref'
        pos = attr_dict.pop('position', 'top')
        outputclass_parts.append(f'tooltip-{pos}')
        
    elif tag_name == 'picture':
        target_tag = 'div'
        outputclass_parts.append('d-picture')

    # Convert generic attributes to outputclass parts
    margin = attr_dict.pop('margin', '')
    if margin:
        for m in margin.split():
            if re.match(r'^[etbsxy]([n-]?\d+|auto)$', m):
                side = m[0]
                val = m[1:].replace('-', 'n')
                outputclass_parts.append(f'm{side}-{val}')
            elif '-' in m:
                outputclass_parts.append(m)
            else:
                outputclass_parts.append(f'm-{m}')
                
    padding = attr_dict.pop('padding', '')
    if padding:
        for p in padding.split():
            if re.match(r'^[etbsxy](\d+|auto)$', p):
                side = p[0]
                val = p[1:]
                outputclass_parts.append(f'p{side}-{val}')
            elif '-' in p:
                outputclass_parts.append(p)
            else:
                outputclass_parts.append(f'p-{p}')
                
    shadow = attr_dict.pop('shadow', '')
    if shadow:
        if shadow == 'yes':
            outputclass_parts.append('shadow')
        elif shadow in ('no', 'none'):
            outputclass_parts.append('shadow-none')
        else:
            outputclass_parts.append(f'shadow-{shadow}')
            
    border = attr_dict.pop('border', '')
    if border:
        if border == 'yes':
            outputclass_parts.append('border')
        elif border == 'no':
            outputclass_parts.append('border-0')
        elif border.isdigit():
            outputclass_parts.append('border')
            outputclass_parts.append(f'border-{border}')
            
    bordercolor = attr_dict.pop('bordercolor', '')
    if bordercolor:
        outputclass_parts.append(f'border-{bordercolor}')
        
    rounded = attr_dict.pop('rounded', '')
    if rounded:
        if rounded == 'yes':
            outputclass_parts.append('rounded')
        elif rounded in ('no', '0'):
            outputclass_parts.append('rounded-0')
        elif rounded in ('circle', 'pill'):
            outputclass_parts.append(f'rounded-{rounded}')
        elif rounded.isdigit():
            outputclass_parts.append(f'rounded-{rounded}')
            
    width = attr_dict.pop('width', '')
    if width:
        outputclass_parts.append(f'w-{width}')
        
    color = attr_dict.pop('color', '')
    if color:
        if target_tag in ('table', 'row', 'entry', 'thead', 'tbody'):
            outputclass_parts.append(f'table-{color}')
        elif target_tag in ('xref', 'link'):
            outputclass_parts.append(f'link-{color}')
        else:
            outputclass_parts.append(f'text-bg-{color}')

    # Special attributes on standard elements
    icon = attr_dict.pop('icon', '')
    if icon:
        otherprops_parts.append(f'icon({icon})')
        
    style_val = attr_dict.pop('style', '')
    if style_val and tag_name != 'tabbed-dialog':
        otherprops_parts.append(f'style({style_val})')

    # Handle image custom attributes in base
    if tag_name == 'image' or target_tag == 'image':
        media = attr_dict.pop('media', '')
        if media:
            otherprops_parts.append(f'media({media})')
        type_attr = attr_dict.pop('type', '')
        if type_attr:
            otherprops_parts.append(f'type({type_attr})')
        loading = attr_dict.pop('loading', '')
        if loading:
            otherprops_parts.append(f'loading({loading})')
            
    # Handle carousel cols attribute
    if tag_name == 'carousel' or target_tag == 'ol':
        cols = attr_dict.pop('cols', '')
        if cols:
            otherprops_parts.append(f'cols({cols})')
            
    # Handle dl colspan attribute
    if tag_name == 'dl' or target_tag == 'dl':
        colspan = attr_dict.pop('colspan', '')
        if colspan:
            otherprops_parts.append(f'cols({colspan})')
            
    # Handle lang -> xml:lang translation
    lang = attr_dict.pop('lang', '')
    if lang:
        attr_dict['xml:lang'] = lang

    # Combine outputclass parts
    existing_outputclass = attr_dict.get('outputclass', '')
    if existing_outputclass:
        outputclass_parts = existing_outputclass.split() + outputclass_parts
        
    if outputclass_parts:
        seen = set()
        distinct_parts = []
        for part in outputclass_parts:
            if part not in seen:
                seen.add(part)
                distinct_parts.append(part)
        attr_dict['outputclass'] = ' '.join(distinct_parts)

    # Combine otherprops parts
    existing_otherprops = attr_dict.get('otherprops', '')
    if existing_otherprops:
        otherprops_parts = existing_otherprops.split() + otherprops_parts
        
    if otherprops_parts:
        seen = set()
        distinct_otherprops = []
        for part in otherprops_parts:
            if part not in seen:
                seen.add(part)
                distinct_otherprops.append(part)
        attr_dict['otherprops'] = ' '.join(distinct_otherprops)

    # Reconstruct the tag
    attrs_str = ''
    for k, v in attr_dict.items():
        attrs_str += f' {k}="{v}"'
        
    res = f'<{target_tag}{attrs_str}'
    if self_closing:
        res += '/'
    res += '>'
    return res

def convert_file(content):
    # Change DTD
    content = re.sub(
        r'<!DOCTYPE\s+topic\s+PUBLIC\s+["\']-//DITA Bootstrap//DTD DITA Bootstrap Topic//EN["\']\s+["\']bootstrap-topic.dtd["\']>',
        r'<!DOCTYPE topic PUBLIC "-//OASIS//DTD DITA Topic//EN" "topic.dtd">',
        content
    )
    
    # Pre-process Table group dividers (move divider="yes" from table to tbody)
    parts = re.split(r'(<codeblock[^>]*>.*?</codeblock>)', content, flags=re.DOTALL)
    
    tag_mapping = {
        'tabbed-dialog': 'bodydiv',
        'accordion': 'bodydiv',
        'accordion-item': 'section',
        'alert': 'section',
        'badge': 'ph',
        'button': 'xref',
        'button-group': 'bodydiv',
        'button-toolbar': 'bodydiv',
        'card': 'section',
        'card-header': 'div',
        'card-footer': 'div',
        'carousel': 'ol',
        'carousel-item': 'li',
        'collapse': 'bodydiv',
        'grid-row': 'bodydiv',  # bodydiv allows block-level children
        'grid-col': 'bodydiv',  # bodydiv allows block-level children
        'list-group': 'ul',
        'offcanvas': 'section',
        'pagination': 'section',
        'popover': 'xref',
        'thumbnail': 'image',
        'tooltip': 'xref',
        'picture': 'div',
        'icon': 'ph'
    }
    
    for i in range(len(parts)):
        if parts[i].startswith('<codeblock'):
            continue
            
        # Table divider pre-processing:
        table_matches = list(re.finditer(r'<table\b[^>]*?\bdivider="yes"[^>]*?>', parts[i]))
        if table_matches:
            for m in reversed(table_matches):
                start_idx = m.end()
                tbody_match = re.search(r'<tbody(\b[^>]*?)?>', parts[i][start_idx:])
                if tbody_match:
                    tbody_start = start_idx + tbody_match.start()
                    tbody_end = start_idx + tbody_match.end()
                    tbody_tag = tbody_match.group(0)
                    tbody_attrs = tbody_match.group(1) or ""
                    if 'outputclass="' in tbody_attrs:
                        new_tbody_tag = re.sub(r'outputclass="([^"]*)"', r'outputclass="\1 table-group-divider"', tbody_tag)
                    else:
                        new_tbody_tag = f'<tbody outputclass="table-group-divider"{tbody_attrs}>'
                    parts[i] = parts[i][:tbody_start] + new_tbody_tag + parts[i][tbody_end:]
            parts[i] = re.sub(r'(\s+divider="yes"|divider="yes"\s+)', '', parts[i])
            
        # Table compact, striped, striped-columns mapping:
        def table_repl(match):
            attrs = match.group(1) or ""
            striped = re.search(r'striped="yes"', attrs)
            striped_cols = re.search(r'striped-columns="yes"', attrs)
            compact = re.search(r'compact="yes"', attrs)
            
            outputclass_addition = []
            if striped:
                outputclass_addition.append('table-striped')
            if striped_cols:
                outputclass_addition.append('table-striped-columns')
            if compact:
                outputclass_addition.append('table-sm')
                
            attrs = re.sub(r'\b(striped|striped-columns|compact)="yes"\s*', '', attrs)
            
            if outputclass_addition:
                addition_str = ' '.join(outputclass_addition)
                if 'outputclass="' in attrs:
                    attrs = re.sub(r'outputclass="([^"]*)"', f'outputclass="\\1 {addition_str}"', attrs)
                else:
                    attrs += f' outputclass="{addition_str}"'
            return f'<table{attrs}>'
            
        parts[i] = re.sub(r'<table(\s+[^>]*?)?>', table_repl, parts[i])

        # Transform start / self-closing tags
        def tag_repl(match):
            tag_name = match.group(1)
            attrs = match.group(2)
            self_closing = match.group(3) is not None
            return transform_tag(tag_name, attrs, self_closing)
            
        parts[i] = re.sub(r'<([a-zA-Z0-9_-]+)(\s+[^>]*?)?(/)?>', tag_repl, parts[i])
        
        # Transform closing tags
        def close_tag_repl(match):
            tag_name = match.group(1)
            target = tag_mapping.get(tag_name, tag_name)
            return f'</{target}>'
            
        parts[i] = re.sub(r'</([a-zA-Z0-9_-]+)>', close_tag_repl, parts[i])
        
    return ''.join(parts)

# Let's run it for all files
# Files excluded from conversion because they contain li > bodydiv nesting
# (carousel-items with nested grid-row/grid-col) which is invalid in standard DITA DTDs.
SKIP_FILES = {'component.dita', 'index.dita', 'carousel.dita'}

for f in spec_files:
    if f in SKIP_FILES:
        continue
    spec_path = os.path.join(spec_dir, f)
    base_path = os.path.join(base_dir, f)
    
    with open(spec_path, 'r', encoding='utf-8') as file:
        orig = file.read()
        
    converted = convert_file(orig)
    
    with open(base_path, 'w', encoding='utf-8') as file:
        file.write(converted)
    print(f"Successfully converted and saved {f}")

# Update document.ditamap in base_dir
map_path = os.path.join(base_dir, "document.ditamap")
with open(map_path, 'r', encoding='utf-8') as file:
    map_content = file.read()

# Replace utilities.dita entry with borders.dita, color.dita, shadows.dita, spacing.dita
if "utilities.dita" in map_content:
    replacement = """<topicref href="borders.dita"/>
    <topicref href="color.dita"/>
    <topicref href="shadows.dita"/>
    <topicref href="spacing.dita"/>"""

    map_content = re.sub(
        r'<topicref\s+href="utilities.dita"\s+navtitle="Borders and Colors"\s+locktitle="yes"\s*/>',
        replacement,
        map_content
    )

    with open(map_path, 'w', encoding='utf-8') as file:
        file.write(map_content)
    print("Updated document.ditamap")

# Delete utilities.dita if it exists
utils_path = os.path.join(base_dir, "utilities.dita")
if os.path.exists(utils_path):
    os.remove(utils_path)
    print("Deleted utilities.dita")
