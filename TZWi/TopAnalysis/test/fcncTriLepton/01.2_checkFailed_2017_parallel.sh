#!/bin/bash
set -u

# Parallel checker for failed jobs in submit_2017
#
# This script scans job directories under submit_2017 in parallel.
# For each directory, it looks into result*.tgz files, searches for an
# archive member whose basename is failed.txt, and appends its content
# to <directory>/failed.txt.
#
# After scanning, it prints all directories that contain failed.txt.
#
# Default parallelism:
#   NPROC=8
#
# Optional override:
#   NPROC=4 ./checkFailed_2017_parallel.sh

: "${NPROC:=16}"

BASE_DIR="submit_2017"

scan_one_dir() {
    local dir="$1"
    local failed_file="$dir/failed.txt"

    # Remove previous output before rescanning
    [ -f "$failed_file" ] && rm -f "$failed_file"

    cd "$dir" || {
        echo "[ERROR] Cannot enter directory: $dir" >&2
        return 1
    }

    shopt -s nullglob
    local tgzs=(result*.tgz)

    # Nothing to do if there are no archives
    if [ "${#tgzs[@]}" -eq 0 ]; then
        return 0
    fi

    local tgz
    local member

    for tgz in "${tgzs[@]}"; do
        # Find the first archive entry whose basename is failed.txt
        member=$(
            tar tzf "$tgz" 2>/dev/null | \
            awk -F/ '
                {
                    n = split($0, a, "/")
                    if (a[n] == "failed.txt") {
                        print $0
                        exit
                    }
                }
            '
        )

        # If such an entry exists, extract that exact member
        if [ -n "$member" ]; then
            tar -Oxzf "$tgz" "$member" >> failed.txt 2>/dev/null
        fi
    done

    # Remove empty failed.txt if created accidentally
    if [ -f failed.txt ] && [ ! -s failed.txt ]; then
        rm -f failed.txt
    fi

    return 0
}

print_one_dir() {
    local dir="$1"
    local failed_file="$dir/failed.txt"

    [ -f "$failed_file" ] || return 0

    echo "============================================================"
    echo "Directory: $dir"
    echo "------------------------------------------------------------"
    cat "$failed_file"
    echo
}

export -f scan_one_dir
export -f print_one_dir

mapfile -d '' DIRS < <(
    find "$BASE_DIR" \
        -mindepth 1 -maxdepth 1 \
        \( -name '*NANOAOD' -o -name '*NANOAODSIM' \) \
        -type d -print0
)

echo "[INFO] Base directory : $BASE_DIR"
echo "[INFO] Target count   : ${#DIRS[@]}"
echo "[INFO] Parallel jobs  : $NPROC"
echo

# Step 1: Scan directories in parallel
printf '%s\0' "${DIRS[@]}" | xargs -0 -n1 -P"$NPROC" bash -c 'scan_one_dir "$1"' _

echo "[INFO] Parallel scan completed."
echo

# Step 2: Print failed job reports sequentially
for dir in "${DIRS[@]}"; do
    print_one_dir "$dir"
done

echo "[INFO] Done."
