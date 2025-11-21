#!/bin/bash

# Build script for umbralcalculations blog
# This script builds HTML pages from Markdown using pandoc

set -e  # Exit on any error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="$SCRIPT_DIR"
PUBLIC_DIR="$DOCS_DIR"
TEMP_DIR="$DOCS_DIR/.temp"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check dependencies
check_dependencies() {
    log_info "Checking dependencies..."
    
    if ! command -v pandoc &> /dev/null; then
        log_error "Missing dependency: pandoc"
        log_info "Install pandoc: https://pandoc.org/installing.html"
        exit 1
    fi
    
    log_success "All dependencies found"
}

# Clean previous build
clean_build() {
    log_info "Cleaning previous build..."
    
    # Remove only generated HTML files, not source files
    if [ -d "$DOCS_DIR/posts" ]; then
        rm -rf "$DOCS_DIR/posts"
    fi
    
    # Note: index.html is the blog homepage and should not be removed
    
    if [ -f "$DOCS_DIR/sitemap.xml" ]; then
        rm -f "$DOCS_DIR/sitemap.xml"
    fi
    
    if [ -f "$DOCS_DIR/robots.txt" ]; then
        rm -f "$DOCS_DIR/robots.txt"
    fi
    
    if [ -f "$DOCS_DIR/posts.json" ]; then
        rm -f "$DOCS_DIR/posts.json"
    fi
    
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi
    
    mkdir -p "$TEMP_DIR"
    
    log_success "Build directory cleaned"
}

# Copy static assets
copy_assets() {
    log_info "Copying static assets..."
    
    # Assets are already in the right place, just ensure they exist
    if [ -d "$DOCS_DIR/assets" ]; then
        log_success "Assets directory found"
    else
        log_warning "Assets directory not found"
    fi
}

# Generate HTML pages
generate_html_pages() {
    log_info "Generating HTML posts..."
    
    # Create posts directory
    mkdir -p "$DOCS_DIR/posts"
    
    # Generate posts from _posts directory
    for filename in "$DOCS_DIR"/_posts/*.md; do
        if [ -f "$filename" ]; then
            local basename=$(basename "$filename" .md)
            local title=$(grep -E '^title:' "$filename" | head -1 | sed 's/title: *"\(.*\)"/\1/' || echo "$basename")
            log_info "Generating post: $basename"
            
            pandoc --template "$DOCS_DIR/template.html" \
                --wrap=preserve \
                --citeproc \
                --csl="$DOCS_DIR/ieee.csl" \
                --bibliography="$DOCS_DIR/biblio.bib" \
                --mathjax \
                --syntax-highlighting=pygments \
                --metadata="title:$title" \
                -f markdown \
                -t html \
                -o "$DOCS_DIR/posts/${basename}.html" \
                "$filename"
        fi
    done
    
    log_success "HTML posts generated"
}

# Generate posts metadata JSON
generate_posts_metadata() {
    log_info "Generating posts metadata..."
    
    local posts_json="$DOCS_DIR/posts.json"
    local temp_dir="$TEMP_DIR/posts_metadata"
    
    # Create temp directory for storing post metadata
    mkdir -p "$temp_dir"
    
    # First pass: extract metadata from all posts
    for filename in "$DOCS_DIR"/_posts/*.md; do
        if [ -f "$filename" ]; then
            local basename=$(basename "$filename" .md)
            local title=$(grep -E '^title:' "$filename" | head -1 | sed 's/title: *"\(.*\)"/\1/' || echo "$basename")
            local tag=$(grep -E '^tag:' "$filename" | head -1 | sed 's/tag: *"\(.*\)"/\1/' || echo "")
            local date=$(grep -E '^date:' "$filename" | head -1 | sed 's/date: *"\(.*\)"/\1/' || echo "")
            local order=$(grep -E '^order:' "$filename" | head -1 | sed 's/order: *\([0-9][0-9]*\).*/\1/' 2>/dev/null)
            if [ -z "$order" ]; then
                order=999
            fi
            
            # Escape JSON special characters in title and tag
            title=$(echo "$title" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g')
            tag=$(echo "$tag" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g')
            
            # Extract images from frontmatter (supports YAML array format)
            # Handles: images: ["img1.jpg", "img2.jpg"] or images: img1.jpg
            local images_json="[]"
            local images_line=$(grep -E '^images:' "$filename" | head -1)
            if [ -n "$images_line" ]; then
                # Check if it's a YAML array format: images: ["img1.jpg", "img2.jpg"]
                if echo "$images_line" | grep -q '\['; then
                    # Use Python to parse the YAML array and convert to JSON
                    images_json=$(echo "$images_line" | python3 -c "
import sys
import re
line = sys.stdin.read().strip()
# Match: images: [\"img1\", \"img2\"]
match = re.search(r'images:\s*\[(.*?)\]', line)
if match:
    content = match.group(1).strip()
    if content:
        # Split by comma, handling quoted strings
        items = []
        current = ''
        in_quotes = False
        for i, char in enumerate(content):
            if char == '\"' and (i == 0 or content[i-1] != '\\\\'):
                in_quotes = not in_quotes
                if not in_quotes:
                    items.append(current.strip('\"').strip())
                    current = ''
                continue
            if in_quotes:
                current += char
        if current.strip():
            items.append(current.strip('\"').strip())
        # Build JSON array
        json_items = [f'\"{item.strip()}\"' for item in items if item.strip()]
        print('[' + ','.join(json_items) + ']')
    else:
        print('[]')
else:
    print('[]')
" 2>/dev/null)
                    # Fallback if Python fails
                    if [ -z "$images_json" ] || [ "$images_json" = "[]" ]; then
                        images_json="[]"
                    fi
                else
                    # Single image: images: img1.jpg or images: "img1.jpg"
                    local single_img=$(echo "$images_line" | sed 's/^images: *"\(.*\)".*/\1/' | sed 's/^images: *\(.*\)/\1/' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | sed 's/^"//;s/"$//')
                    if [ -n "$single_img" ]; then
                        images_json="[\"$single_img\"]"
                    fi
                fi
            fi
            
            # Write post metadata to temp file with order prefix for sorting
            # Format: ORDER_BASENAME.json (padded order for proper numeric sort)
            local order_padded=$(printf "%04d" "$order")
            cat > "$temp_dir/${order_padded}_${basename}.json" << EOF
  {
    "title": "$title",
    "slug": "$basename",
    "url": "/posts/$basename.html",
    "tag": "$tag",
    "date": "$date",
    "order": $order,
    "images": $images_json
  }
EOF
        fi
    done
    
    # Sort posts by order (numeric sort on filename prefix) and combine into JSON array
    echo "[" > "$posts_json"
    local first=true
    for json_file in $(ls -1 "$temp_dir"/*.json 2>/dev/null | sort); do
        if [ -f "$json_file" ]; then
            if [ "$first" = true ]; then
                first=false
            else
                echo "," >> "$posts_json"
            fi
            cat "$json_file" >> "$posts_json"
        fi
    done
    echo "]" >> "$posts_json"
    
    # Clean up temp directory
    rm -rf "$temp_dir"
    
    log_success "Posts metadata generated"
}

# Generate sitemap
generate_sitemap() {
    log_info "Generating sitemap..."
    
    local base_url="https://umbralcalc.github.io"
    
    cat > "$DOCS_DIR/sitemap.xml" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>$base_url/</loc>
    <lastmod>$(date -u +%Y-%m-%d)</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
EOF
    
    # Add posts
    for file in "$DOCS_DIR"/posts/*.html; do
        if [ -f "$file" ]; then
            local filename=$(basename "$file")
            cat >> "$DOCS_DIR/sitemap.xml" << EOF
  <url>
    <loc>$base_url/posts/$filename</loc>
    <lastmod>$(date -u +%Y-%m-%d)</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
EOF
        fi
    done
    
    # Add CV page
    if [ -f "$DOCS_DIR/cv.html" ]; then
        cat >> "$DOCS_DIR/sitemap.xml" << EOF
  <url>
    <loc>$base_url/cv.html</loc>
    <lastmod>$(date -u +%Y-%m-%d)</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
EOF
    fi
    
    cat >> "$DOCS_DIR/sitemap.xml" << EOF
</urlset>
EOF
    
    log_success "Sitemap generated"
}

# Generate robots.txt
generate_robots() {
    log_info "Generating robots.txt..."
    
    cat > "$DOCS_DIR/robots.txt" << EOF
User-agent: *
Allow: /

Sitemap: https://umbralcalc.github.io/sitemap.xml
EOF
    
    log_success "robots.txt generated"
}

# Validate build
validate_build() {
    log_info "Validating build..."
    
    local errors=0
    
    # Check if main files exist
    if [ ! -f "$DOCS_DIR/index.html" ]; then
        log_error "index.html not found"
        ((errors++))
    fi
    
    if [ ! -d "$DOCS_DIR/assets" ]; then
        log_error "assets directory not found"
        ((errors++))
    fi
    
    # Check for broken links (basic check)
    for html_file in "$DOCS_DIR"/posts/*.html; do
        if [ -f "$html_file" ]; then
            # This is a basic check - in production you might want to use a proper link checker
            if grep -q "href=\"#" "$html_file"; then
                log_warning "Potential broken internal links in $(basename "$html_file")"
            fi
        fi
    done
    
    if [ $errors -eq 0 ]; then
        log_success "Build validation passed"
    else
        log_error "Build validation failed with $errors errors"
        exit 1
    fi
}

# Main build function
main() {
    log_info "Starting simplified documentation build..."
    
    check_dependencies
    clean_build
    copy_assets
    generate_html_pages
    generate_posts_metadata
    generate_sitemap
    generate_robots
    validate_build
    
    # Clean up temporary files
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
        log_info "Cleaned up temporary files"
    fi
    
    log_success "Documentation build completed successfully!"
    log_info "Output directory: $DOCS_DIR"
    log_info "You can now serve the documentation with:"
    log_info "  cd $DOCS_DIR && python3 -m http.server 8000"
    log_info "  or"
    log_info "  cd $DOCS_DIR && npx serve ."
}

# Run main function
main "$@"
