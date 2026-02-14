"""
Flask Web Server for CrewAI Multi-Agent Research System
Provides REST API and Server-Sent Events for real-time updates
"""
from flask import Flask, render_template, request, jsonify, Response
from src.crew import create_crew
import threading
import time
import queue
import json

app = Flask(__name__)

# Global queue for storing progress updates
progress_queue = queue.Queue()
current_status = {"status": "idle", "message": "", "result": None}


def run_research(topic):
    """
    Execute CrewAI research in a background thread
    
    Args:
        topic (str): Research topic to process
    """
    global current_status
    
    try:
        # Update status
        current_status = {"status": "running", "message": f"Starting research on: {topic}", "result": None}
        progress_queue.put(json.dumps(current_status))
        
        # Create crew
        progress_queue.put(json.dumps({
            "status": "running",
            "message": "🤖 Initializing AI agents...",
            "result": None
        }))
        crew = create_crew()
        
        # Start research
        progress_queue.put(json.dumps({
            "status": "running",
            "message": "🔍 Senior Researcher analyzing the topic...",
            "result": None
        }))
        
        # Execute crew
        result = crew.kickoff(inputs={'topic': topic})
        
        # Complete
        current_status = {
            "status": "completed",
            "message": "✅ Research completed successfully!",
            "result": str(result)
        }
        progress_queue.put(json.dumps(current_status))
        
    except Exception as e:
        error_msg = f"Error during research: {str(e)}"
        current_status = {
            "status": "error",
            "message": error_msg,
            "result": None
        }
        progress_queue.put(json.dumps(current_status))


@app.route('/')
def index():
    """Render the main web interface"""
    return render_template('index.html')


@app.route('/api/research', methods=['POST'])
def start_research():
    """
    API endpoint to start research on a topic
    
    Request JSON:
        {
            "topic": "research topic here"
        }
    
    Returns:
        JSON response with status
    """
    data = request.json
    topic = data.get('topic', '').strip()
    
    if not topic:
        return jsonify({"error": "Topic is required"}), 400
    
    # Check if already running
    if current_status.get("status") == "running":
        return jsonify({"error": "Research already in progress"}), 409
    
    # Start research in background thread
    thread = threading.Thread(target=run_research, args=(topic,))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        "status": "started",
        "message": f"Research started for topic: {topic}"
    })


@app.route('/api/stream')
def stream():
    """
    Server-Sent Events endpoint for real-time progress updates
    
    Returns:
        SSE stream with progress updates
    """
    def generate():
        """Generate SSE messages from the progress queue"""
        # Send initial status
        yield f"data: {json.dumps(current_status)}\n\n"
        
        # Stream updates
        while True:
            try:
                # Get update from queue (with timeout to allow checking)
                message = progress_queue.get(timeout=1)
                yield f"data: {message}\n\n"
            except queue.Empty:
                # Send heartbeat to keep connection alive
                yield f"data: {json.dumps({'status': 'heartbeat'})}\n\n"
            except GeneratorExit:
                # Client disconnected
                break
    
    return Response(generate(), mimetype='text/event-stream')


@app.route('/api/status')
def get_status():
    """
    Get current research status
    
    Returns:
        JSON with current status
    """
    return jsonify(current_status)


if __name__ == '__main__':
    print("=" * 60)
    print("CrewAI Multi-Agent Research System - Web Interface")
    print("=" * 60)
    print("\n🌐 Starting Flask server...")
    print("📍 Open your browser and navigate to: http://localhost:5000")
    print("\n" + "=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
