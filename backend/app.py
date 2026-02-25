# ...existing code...
from flask import Flask, send_from_directory, jsonify, request, abort
from flask_cors import CORS
import os, json, re, threading, traceback, logging

# Serve frontend static files
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)
app.logger.setLevel(logging.INFO)

# Candidate locations for exams.json (do not modify project structure)
DB_CANDIDATES = [
    os.path.join(os.path.dirname(__file__), 'database', 'exams.json'),
    os.path.join(BASE_DIR, 'database', 'exams.json'),                # include top-level /database/exams.json
    os.path.join(BASE_DIR, 'frontend', 'database', 'exams.json'),
    os.path.join(BASE_DIR, 'frontend', 'assets', 'exams.json'),
]

EXAMS_LOCK = threading.Lock()
EXAMS = []

def _find_exams_file():
    for p in DB_CANDIDATES:
        p = os.path.normpath(p)
        if os.path.exists(p):
            app.logger.info('Using exams file: %s', p)
            return p
    app.logger.warning('No exams.json found in candidates: %s', DB_CANDIDATES)
    return None

def convert_exam_format(raw_list):
    out = []
    for idx, r in enumerate(raw_list, start=1):
        name = r.get('name') or r.get('Exam Name') or r.get('title') or ''
        category = r.get('category') or r.get('Category') or ''
        level = r.get('level') or r.get('Level') or ''
        purpose = r.get('purpose') or r.get('Purpose') or ''
        exam_mode = r.get('mode') or r.get('Mode') or ''
        syllabus = r.get('syllabus') or r.get('Syllabus (Summary)') or ''
        app_date = r.get('Application Date') or r.get('applicationDate') or r.get('Application Date (2025)') or ''
        exam_month = r.get('Exam -month') or r.get('examMonth') or ''
        website = r.get('Official website') or r.get('website') or ''
        fee = r.get('Application fee') or r.get('applicationFee') or ''
        youtube_ref = r.get('youtube referrence links') or r.get('youtubeReference') or ''
        
        # stream: explicit or extracted from parentheses in category
        stream = ''
        if r.get('stream'):
            stream_val = r.get('stream')
            if isinstance(stream_val, str):
                stream = stream_val
            elif isinstance(stream_val, list) and stream_val:
                stream = stream_val[0]
        else:
            m = re.search(r'\(([^)]+)\)', category or '')
            stream = m.group(1).strip() if m else ''
        slug = r.get('slug') or (name.lower().replace(' ', '-')) if name else None
        ex_id = r.get('id') or r.get('_id') or str(idx)
        out.append({
            'id': str(ex_id),
            'slug': slug,
            'name': name,
            'category': category,
            'level': level,
            'stream': stream,
            'examDates': r.get('examDates') or r.get('Exam Dates') or [],
            'purpose': purpose,
            'mode': exam_mode,
            'syllabus': syllabus,
            'applicationDate': app_date,
            'examMonth': exam_month,
            'website': website,
            'applicationFee': fee,
            'youtubeReference': youtube_ref,
            '_raw': r
        })
    return out

def load_exams_from_file():
    try:
        f = _find_exams_file()
        if not f:
            app.logger.warning('exams.json not found; returning empty list.')
            return []
        with open(f, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        raw_list = data.get('exams') if isinstance(data, dict) and 'exams' in data else data
        if not isinstance(raw_list, list):
            app.logger.warning('exams.json does not contain a list; returning empty list.')
            return []
        return convert_exam_format(raw_list)
    except Exception as e:
        app.logger.error('load_exams_from_file error: %s\n%s', e, traceback.format_exc())
        return []

def refresh_cache():
    global EXAMS
    with EXAMS_LOCK:
        EXAMS = load_exams_from_file() or []
    app.logger.info('EXAMS cache refreshed: %d records', len(EXAMS))

# Initialize cache at startup
refresh_cache()

def map_category_to_level(category):
    if not category: return ''
    c = category.lower()
    if '10th' in c or re.search(r'\b10\b', c): return 'After 10'
    if '12th' in c or re.search(r'\b12\b', c): return 'After 12'
    if 'diploma' in c: return 'After Diploma'
    if 'undergrad' in c or 'ug' in c: return 'After UG'
    if 'postgrad' in c or 'pg' in c: return 'After PG'
    return category.strip()

# Static file routes
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:filename>')
def static_files(filename):
    # don't capture API routes
    if filename.startswith('api/'):
        abort(404)
    file_path = os.path.join(FRONTEND_DIR, filename)
    if os.path.exists(file_path):
        return send_from_directory(FRONTEND_DIR, filename)
    # SPA fallback
    return app.send_static_file('index.html')

# API: build dropdown data from EXAMS cache
@app.route('/api/dropdown-data', methods=['GET'])
def dropdown_data():
    try:
        with EXAMS_LOCK:
            snapshot = list(EXAMS)
        levels_map = {}
        streams_map = {}
        substreams_map = {}
        for ex in snapshot:
            category = ex.get('category') or ''
            name = ex.get('name') or ''
            if not category or not name:
                continue
            level_name = map_category_to_level(category)
            level_id = (level_name or category).lower().replace(' ', '_') or 'general'
            levels_map[level_id] = level_name or category

            stream_name = ex.get('stream') or ''
            if not stream_name:
                m = re.search(r'\(([^)]+)\)', category or '')
                stream_name = m.group(1).strip() if m else 'General'
            stream_id = (stream_name or 'general').lower().replace(' ', '_')

            streams_map.setdefault(level_id, {})
            streams_map[level_id][stream_id] = stream_name

            key = f"{level_id}||{stream_id}"
            substreams_map.setdefault(key, set()).add(name)

        levels_out = [{'id': k, 'name': v} for k, v in sorted(levels_map.items(), key=lambda x: x[1])]
        streams_out = { lid: [{'id': sid, 'name': sname} for sid, sname in sorted(sdict.items(), key=lambda x: x[1])] for lid, sdict in streams_map.items() }
        substreams_out = { key: [{'id': s.lower().replace(' ', '-'), 'name': s} for s in sorted(list(sset))] for key, sset in substreams_map.items() }

        return jsonify({'success': True, 'data': {'levels': levels_out, 'streams': streams_out, 'substreams': substreams_out}})
    except Exception as e:
        app.logger.error('dropdown_data error: %s\n%s', e, traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500

# API: list exams filtered by query params
@app.route('/api/exams', methods=['GET'])
def get_exams():
    try:
        q_level = (request.args.get('level') or request.args.get('category') or '').strip()
        q_stream = (request.args.get('stream') or '').strip()
        q_sub = (request.args.get('subStream') or '').strip()
        q_search = (request.args.get('search') or '').strip()

        with EXAMS_LOCK:
            snapshot = list(EXAMS)

        results = []
        for ex in snapshot:
            name = ex.get('name') or ''
            category = ex.get('category') or ''
            level = ex.get('level') or map_category_to_level(category)
            stream = ex.get('stream') or ''
            if not stream:
                m = re.search(r'\(([^)]+)\)', category or '')
                stream = m.group(1).strip() if m else ''

            # Apply search filter - search in name and category
            if q_search:
                q = q_search.lower()
                if q not in name.lower() and q not in category.lower():
                    continue
            
            # Apply level filter - match against level field
            if q_level:
                q = q_level.lower()
                # Check if level matches exactly or partially
                if q not in level.lower():
                    continue
            
            # Apply stream filter - match against stream field
            if q_stream:
                q = q_stream.lower()
                # If stream is empty (not derived from category), and user selected "general", include it
                if stream:
                    if q not in stream.lower() and q not in category.lower():
                        continue
                else:
                    # For exams without specific stream, only accept "general"
                    if q != 'general':
                        continue
            
            # Apply substream filter - match against name field
            if q_sub:
                q = q_sub.lower()
                if q not in name.lower():
                    continue

            results.append({
                'id': ex.get('id'),
                'slug': ex.get('slug'),
                'name': name,
                'level': level,
                'category': category,
                'stream': stream,
                'examDates': ex.get('examDates') or [],
                'purpose': ex.get('purpose') or '',
                'mode': ex.get('mode') or '',
                'syllabus': ex.get('syllabus') or '',
                'applicationDate': ex.get('applicationDate') or '',
                'examMonth': ex.get('examMonth') or '',
                'website': ex.get('website') or '',
                'applicationFee': ex.get('applicationFee') or '',
                'youtubeReference': ex.get('youtubeReference') or ''
            })

        return jsonify({'status': 'success', 'exams': results, 'total': len(results)})
    except Exception as e:
        app.logger.error('list_exams error: %s\n%s', e, traceback.format_exc())
        return jsonify({'status': 'error', 'message': str(e)}), 500

# API: get single exam details by slug
@app.route('/api/exams/<slug>', methods=['GET'])
def get_exam_by_slug(slug):
    try:
        with EXAMS_LOCK:
            snapshot = list(EXAMS)
        
        for ex in snapshot:
            if ex.get('slug') == slug:
                return jsonify({'status': 'success', 'exam': {
                    'id': ex.get('id'),
                    'slug': ex.get('slug'),
                    'name': ex.get('name') or '',
                    'level': ex.get('level') or '',
                    'category': ex.get('category') or '',
                    'stream': ex.get('stream') or '',
                    'examDates': ex.get('examDates') or [],
                    'purpose': ex.get('purpose') or '',
                    'mode': ex.get('mode') or '',
                    'syllabus': ex.get('syllabus') or '',
                    'applicationDate': ex.get('applicationDate') or '',
                    'examMonth': ex.get('examMonth') or '',
                    'website': ex.get('website') or '',
                    'applicationFee': ex.get('applicationFee') or '',
                    'youtubeReference': ex.get('youtubeReference') or ''
                }})
        
        return jsonify({'status': 'error', 'message': 'Exam not found'}), 404
    except Exception as e:
        app.logger.error('get_exam_by_slug error: %s\n%s', e, traceback.format_exc())
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Admin: refresh cache without restart
@app.route('/api/admin/reload', methods=['POST'])
def admin_reload():
    refresh_cache()
    return jsonify({'success': True, 'total': len(EXAMS)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
# ...existing code...