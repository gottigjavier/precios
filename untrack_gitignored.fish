#!/usr/bin/env fish

for file in (jj file list)
    if test -d "$file"
        continue
    end

    set basename (basename "$file")

    if string match -q "*__pycache__*" "$file"
        echo "Untracking: $file"
        jj file untrack "$file" 2>/dev/null
    else if string match -q "*.pyc" "$basename"
        echo "Untracking: $file"
        jj file untrack "$file" 2>/dev/null
    else if string match -q "resultados.*" "$basename"
        echo "Untracking: $file"
        jj file untrack "$file" 2>/dev/null
    else if string match -q "test*" "$basename"
        echo "Untracking: $file"
        jj file untrack "$file" 2>/dev/null
    end
end

echo "Done!"
