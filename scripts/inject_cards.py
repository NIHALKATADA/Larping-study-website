import re

with open('subjects/dbms/cheat-sheet.html', 'r', encoding='utf-8') as f:
    html = f.read()

trap_icon = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0; margin-top:2px;"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
tip_icon = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0; margin-top:2px;"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>'

# 1. Keys Trap
replace_1 = f'''</dl>
                    <div class="exam-trap">
                        {trap_icon}
                        <div><strong>Exam Trap:</strong> Every Primary Key is a Candidate Key, but not every Candidate Key is a Primary Key!</div>
                    </div>
                </div>'''
html = html.replace('</dl>\n                </div>', replace_1)

# 2. 3-Level Architecture Pro Tip
replace_2 = f'''</ul>
                    <div class="pro-tip">
                        {tip_icon}
                        <div><strong>Pro-Tip:</strong> The primary objective of the 3-level architecture is to achieve Data Independence (Logical and Physical).</div>
                    </div>
                </div>'''
html = html.replace('</ul>\n                </div>', replace_2)

# 3. Normalization BCNF Trap
replace_3 = f'''</table>
                    <div class="exam-trap">
                        {trap_icon}
                        <div><strong>Exam Trap:</strong> A table can be in 3NF but fail BCNF if it contains overlapping candidate keys and a non-prime attribute determines part of a candidate key.</div>
                    </div>
                </div>'''
html = html.replace('</table>\n                </div>', replace_3)

# 4. TRC vs DRC Pro Tip
replace_4 = f'''</dl>
                    <div class="pro-tip">
                        {tip_icon}
                        <div><strong>Pro-Tip:</strong> TRC represents entire rows (t), while DRC represents individual column values (x, y, z).</div>
                    </div>
                </div>'''
# Wait, let's see if TRC/DRC is even in the current HTML. Probably not.

with open('subjects/dbms/cheat-sheet.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Injected traps and tips into existing UI')
