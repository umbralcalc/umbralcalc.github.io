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
    
    # Start JSON array
    echo "[" > "$posts_json"
    
    local first=true
    for filename in "$DOCS_DIR"/_posts/*.md; do
        if [ -f "$filename" ]; then
            local basename=$(basename "$filename" .md)
            local title=$(grep -E '^title:' "$filename" | head -1 | sed 's/title: *"\(.*\)"/\1/' || echo "$basename")
            local tag=$(grep -E '^tag:' "$filename" | head -1 | sed 's/tag: *"\(.*\)"/\1/' || echo "")
            local date=$(grep -E '^date:' "$filename" | head -1 | sed 's/date: *"\(.*\)"/\1/' || echo "")
            
            # Escape JSON special characters in title and tag
            title=$(echo "$title" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g')
            tag=$(echo "$tag" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g')
            local excerpt_field=$(grep -E '^excerpt:' "$filename" | head -1 | sed 's/excerpt: *"\(.*\)"/\1/' || echo "")
            
            # Extract excerpt from frontmatter or first paragraph
            local excerpt=""
            if [ -n "$excerpt_field" ]; then
                excerpt="$excerpt_field"
            else
                # Get first paragraph after frontmatter (skip headings, code blocks, HTML, empty lines)
                excerpt=$(awk '
                    BEGIN { in_frontmatter=0; in_para=0; para=""; seen="" }
                    /^---$/ { 
                        if (in_frontmatter) { in_frontmatter=0; next }
                        else { in_frontmatter=1; next }
                    }
                    in_frontmatter { next }
                    /^#/ { next }
                    /^```/ { next }
                    /^<div/ { next }
                    /^<\/div>/ { next }
                    /^$/ { 
                        if (in_para && length(para) > 0) { 
                            # Check if we already have this content
                            if (index(seen, para) == 0) {
                                print para
                                seen = seen para
                            }
                            exit 
                        }
                        in_para=0
                        para=""
                        next 
                    }
                    NF && !in_para && !/^</ { in_para=1 }
                    in_para && !/^</ { 
                        para = para (para ? " " : "") $0
                        if (length(para) > 200) { 
                            print substr(para, 1, 200)
                            exit 
                        }
                    }
                    END { if (in_para && length(para) > 0 && index(seen, para) == 0) print para }
                ' "$filename" | tr '\n' ' ' | sed 's/"/\\"/g' | sed 's/\\n/ /g' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | sed 's/[[:space:]]\+/ /g')
            fi
            
            # Escape JSON special characters in excerpt
            excerpt=$(echo "$excerpt" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | sed 's/\t/\\t/g' | sed 's/\r/\\r/g')
            
            if [ "$first" = true ]; then
                first=false
            else
                echo "," >> "$posts_json"
            fi
            
            cat >> "$posts_json" << EOF
  {
    "title": "$title",
    "slug": "$basename",
    "url": "/posts/$basename.html",
    "tag": "$tag",
    "date": "$date",
    "excerpt": "$excerpt"
  }
EOF
        fi
    done
    
    echo "]" >> "$posts_json"
    
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
