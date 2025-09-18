# Meeting Transcription Module

A comprehensive meeting transcription and management system integrated with your AI agent. This module provides real-time audio transcription, meeting management, and automatic PDF generation.

## 🚀 Features

- **Real-time Audio Transcription**: Continuous audio recording and transcription
- **Meeting Management**: Create, start, end, and manage meetings
- **Participant Tracking**: Add and manage meeting participants with roles and departments
- **Automatic PDF Generation**: Professional meeting summaries with timestamps
- **Database Storage**: SQLite database for meeting history and search
- **AI Agent Integration**: Seamlessly integrated with your existing AI agent
- **Voice Command Detection**: Automatic meeting start/end detection
- **Backup System**: Raw audio backup and fallback text summaries

## 📁 Folder Structure

```
meetings/
├── active/          # Currently active meeting files
├── completed/       # Generated PDF/TXT summaries
└── backup/          # Raw audio chunks and backup files
```

## 🛠️ Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Required Packages**:
   - `pyaudio` - Audio recording
   - `reportlab` - PDF generation
   - `wave` - Audio file handling
   - `livekit-agents` - AI agent integration

## 🎯 Usage

### Starting a Meeting

Your AI agent can start a meeting using voice commands or direct function calls:

```python
# AI Agent will automatically detect: "start the meeting"
# Then ask for meeting details:
# - Meeting topic
# - Main discussion points
# - Keywords
# - Participants list
```

**Voice Commands**:
- "Start the meeting" → Triggers meeting initialization
- "End the meeting" → Triggers meeting completion

### Meeting Flow

1. **Initialize**: AI agent asks for meeting details
2. **Start Recording**: Audio transcription begins automatically
3. **Real-time Processing**: Continuous transcription with speaker identification
4. **End Meeting**: AI agent confirms and generates summary
5. **Generate PDF**: Professional summary with all details

## 🔧 Function Tools Available

### Core Meeting Functions

| Function | Description | Parameters |
|----------|-------------|------------|
| `start_meeting` | Start a new meeting | `meeting_topic`, `main_topics`, `keywords`, `members_list` |
| `end_meeting` | End current meeting | `meeting_id` (optional) |
| `get_current_meeting_status` | Get active meeting status | None |

### Management Functions

| Function | Description | Parameters |
|----------|-------------|------------|
| `add_meeting_participant` | Add participant | `meeting_id`, `name`, `role`, `department` |
| `get_meeting_details` | Get meeting info | `meeting_id` |
| `search_meetings` | Search meetings | `query`, `search_fields` |
| `get_all_meetings` | List all meetings | `status`, `limit` |

### CRUD Operations

| Function | Description | Parameters |
|----------|-------------|------------|
| `update_meeting` | Update meeting details | `meeting_id`, various fields |
| `delete_meeting` | Delete meeting | `meeting_id` |

## 🎙️ Audio Transcription

### How It Works

1. **Audio Capture**: Uses PyAudio to capture microphone input
2. **Chunk Processing**: Processes audio in 5-second chunks
3. **AI Transcription**: Integrates with your AI agent's STT capabilities
4. **Real-time Storage**: Saves transcriptions to database immediately
5. **Backup**: Stores raw audio chunks for recovery

### Audio Settings

- **Sample Rate**: 16kHz
- **Channels**: Mono (1)
- **Format**: 16-bit PCM
- **Chunk Size**: 1024 frames
- **Processing Interval**: Every 5 seconds

## 📊 Database Schema

### Meetings Table
```sql
CREATE TABLE meetings (
    meeting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_topic TEXT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    duration_minutes INTEGER,
    status TEXT DEFAULT 'active',
    file_path TEXT,
    file_size INTEGER,
    main_topics TEXT,
    keywords TEXT,
    members_list TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Meeting Transcripts Table
```sql
CREATE TABLE meeting_transcripts (
    transcript_id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER,
    speaker_name TEXT,
    timestamp DATETIME,
    text_content TEXT,
    FOREIGN KEY (meeting_id) REFERENCES meetings (meeting_id)
);
```

### Meeting Participants Table
```sql
CREATE TABLE meeting_participants (
    participant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER,
    name TEXT NOT NULL,
    role TEXT,
    department TEXT,
    join_time DATETIME,
    leave_time DATETIME,
    FOREIGN KEY (meeting_id) REFERENCES meetings (meeting_id)
);
```

## 📄 PDF Generation

### PDF Structure

1. **Meeting Details**: ID, topic, time, duration, status
2. **Participants**: Name, role, department
3. **Discussion Points**: Main topics and keywords
4. **Transcript Summary**: Organized by minute with speaker identification

### Fallback Options

- **Primary**: PDF generation with ReportLab
- **Fallback**: Text file if PDF generation fails
- **Backup**: Raw audio chunks for manual processing

## 🔍 Search and Retrieval

### Search Capabilities

- **Topic Search**: Find meetings by topic
- **Keyword Search**: Search within main topics and keywords
- **Participant Search**: Find meetings by participant
- **Date Range**: Filter by meeting dates
- **Status Filter**: Active, completed, or cancelled meetings

### AI Integration

Your AI agent can:
- Search past meetings for context
- Retrieve meeting summaries
- Answer questions about previous meetings
- Provide meeting history and insights

## 🚨 Error Handling

### Common Issues

1. **Microphone Access**: Handles permission errors gracefully
2. **Audio Quality**: Implements noise reduction and enhancement
3. **Transcription Failures**: Falls back to text summaries
4. **PDF Generation**: Automatic fallback to text files
5. **Database Errors**: Comprehensive error logging and recovery

### Recovery Features

- **Auto-save**: Every 5 minutes during transcription
- **Backup Audio**: Raw audio chunks for manual processing
- **Transaction Rollback**: Database operation safety
- **Graceful Degradation**: System continues working with reduced functionality

## 🧪 Testing

Run the test script to verify functionality:

```bash
python test_meeting_module.py
```

This will test:
- Database operations
- Meeting creation and management
- Participant management
- Transcript handling
- Search functionality
- PDF generation (simulated)

## 🔧 Configuration

### Environment Variables

Add these to your `.env` file:

```env
# Audio settings
AUDIO_SAMPLE_RATE=16000
AUDIO_CHUNK_SIZE=1024
AUDIO_PROCESSING_INTERVAL=5

# File paths
MEETINGS_DB_PATH=meetings.db
MEETINGS_FOLDER=meetings/
BACKUP_FOLDER=meetings/backup/
```

### Customization

- **Audio Quality**: Adjust sample rate and chunk size
- **Processing Interval**: Change transcription frequency
- **PDF Format**: Customize PDF styling and layout
- **Database**: Use different database systems

## 📈 Performance

### Optimization Features

- **Asynchronous Processing**: Non-blocking audio recording
- **Chunked Processing**: Efficient memory usage
- **Database Indexing**: Fast search and retrieval
- **File Compression**: Optimized storage usage

### Scalability

- **Modular Design**: Easy to extend and modify
- **Database Optimization**: Efficient queries and indexing
- **Memory Management**: Minimal memory footprint
- **Multi-threading**: Concurrent audio and processing

## 🔮 Future Enhancements

### Planned Features

- **Speaker Recognition**: AI-powered voice identification
- **Language Support**: Multi-language transcription
- **Cloud Storage**: Integration with cloud services
- **Advanced Analytics**: Meeting insights and metrics
- **Integration APIs**: Connect with calendar and video platforms

### Custom Development

The modular design allows easy addition of:
- New transcription engines
- Custom PDF templates
- Advanced search algorithms
- Integration with external services

## 🆘 Troubleshooting

### Common Problems

1. **PyAudio Installation Issues**:
   ```bash
   # Windows
   pip install pipwin
   pipwin install pyaudio
   
   # Linux
   sudo apt-get install python3-pyaudio
   
   # macOS
   brew install portaudio
   pip install pyaudio
   ```

2. **Microphone Access**:
   - Check system permissions
   - Verify microphone is working
   - Test with other applications

3. **Database Errors**:
   - Check file permissions
   - Verify SQLite installation
   - Check disk space

### Support

For issues or questions:
1. Check the logs in your console
2. Verify all dependencies are installed
3. Test with the provided test script
4. Check file permissions and paths

## 📝 License

This module is part of your AI agent system and follows the same licensing terms.

---

**🎉 Your AI agent now has powerful meeting transcription capabilities!**

Start using it by saying "start the meeting" and let the AI handle everything else. 