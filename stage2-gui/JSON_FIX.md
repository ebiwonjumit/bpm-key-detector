# JSON Serialization Fix

## Problem

The Python analyzer was failing when outputting JSON because numpy types (float32, int32, etc.) are not directly JSON serializable.

**Error**:
```
Object of type float32 is not JSON serializable
```

This affected the Stage 2 GUI because it uses the `--json` flag to get structured output from the Python backend.

## Solution

Added a custom JSON encoder to handle numpy types:

```python
class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types."""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)
```

Updated all `json.dumps()` and `json.dump()` calls to use this encoder:

```python
json.dumps(results, indent=2, cls=NumpyEncoder)
```

## Files Changed

- `stage2-gui/python-backend/analyzer.py` - Added NumpyEncoder and updated JSON calls
- `stage1-cli/src/analyzer.py` - Same fix applied

## Testing

Test that JSON output works:

```bash
# Stage 2 backend
stage2-gui/python-backend/venv/bin/python3 \
  stage2-gui/python-backend/analyzer.py \
  --file samples/forgetExist.mp3 --json

# Stage 1 CLI
stage1-cli/venv/bin/python3 \
  stage1-cli/src/analyzer.py \
  --file samples/forgetExist.mp3 --json
```

Both should output valid JSON without errors.

## Result

✅ Stage 1 CLI JSON output works
✅ Stage 2 GUI can now parse Python backend output
✅ Batch processing CSV/JSON export works
✅ All numeric types properly serialized

The Stage 2 GUI should now successfully analyze audio files!
