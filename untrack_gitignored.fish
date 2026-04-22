#!/usr/bin/env fish

set gitignore_file ".gitignore"

if not test -f $gitignore_file
    echo "Error: $gitignore_file not found"
    exit 1
end

set temp_file (mktemp)
grep -v '^#' $gitignore_file | grep -v '^$' > $temp_file

while read -l pattern
    set pattern (string trim $pattern)

    if test -z $pattern
        continue
    end

    if string match -q '*/' $pattern
        set dir_pattern (string replace -r '[/\\*]+$' '' $pattern)
        if test -d "$dir_pattern"
            echo "Untracking directory: $dir_pattern/"
            jj file untrack "$dir_pattern/" 2>/dev/null
        end
    else if string match -q '*' $pattern
        for file in (ls -1 $pattern 2>/dev/null)
            if test -e "$file"
                echo "Untracking: $file"
                jj file untrack "$file" 2>/dev/null
            end
        end
    else
        if test -e "$pattern"
            if test -d "$pattern"
                echo "Untracking directory: $pattern/"
                jj file untrack "$pattern/" 2>/dev/null
            else
                echo "Untracking: $pattern"
                jj file untrack "$pattern" 2>/dev/null
            end
        end
    end
end < $temp_file

rm $temp_file

echo "Done! Run 'jj st' to verify changes."
