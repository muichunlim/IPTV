# IPTV Playlist Generator

This tool fetches a remote M3U playlist, filters it, and reorganizes the channels according to specific preferences. It is designed to prioritize Singapore and Malaysia channels while maintaining a clean list of other customized groups.

## Features

- **Fetch & Retry**: Downloads the playlist from a configured source with automatic retry logic (up to 2 retries).
- **Validation**: Ensures the fetched playlist is valid and contains sufficient data (minimum 100 lines).
- **Smart Filtering**:
  - Breaks down "Other" (其它) categories to identify and extract Singapore and Malaysia channels.
  - Filters out channels that do not match the specified keywords for these regions.
- **Reordering**: Sorts channels based on a predefined group priority, placing Singapore and Malaysia channels at the top.
- **Clean Output**: Generates a finalized `tv.m3u` file ready for use.

## Configuration

- **Source URL**: `https://live.catvod.com/tv.m3u`
- **Output File**: `tv.m3u`

## Usage

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Script**:
   ```bash
   python gen_m3u.py
   ```

## processing Logic

1. **Reorder**: Channels are organized based on the `GROUP_ORDER` list.
2. **Extract**: "Singapore" and "Malaysia" channels hidden in "Other" groups are identified using specific keywords (e.g., "CNA", "8TV", "Channel 8").
3. **Filter**: Non-matching channels in specific groups are discarded to keep the list relevant (focusing on Chinese, Cantonese, and English content).
