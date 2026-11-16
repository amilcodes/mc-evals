// Records ONE window (the Minecraft window of a given process id) to an H.264 .mp4 with
// ScreenCaptureKit. Nothing outside that window is captured, and it keeps recording when the
// window is covered by other windows.
//
//   WindowRecorder <pid> <seconds> <out.mp4> [fps]
//
// It refuses to record unless exactly the target process owns a window whose title contains
// "Minecraft"; it never falls back to the display.
import AppKit
import AVFoundation
import CoreMedia
import Foundation
import ScreenCaptureKit

final class Recorder: NSObject, SCStreamOutput, SCStreamDelegate {
    let writer: AVAssetWriter
    let input: AVAssetWriterInput
    var started = false
    var frames = 0
    let lock = NSLock()

    init(url: URL, width: Int, height: Int) throws {
        try? FileManager.default.removeItem(at: url)
        writer = try AVAssetWriter(outputURL: url, fileType: .mp4)
        let settings: [String: Any] = [
            AVVideoCodecKey: AVVideoCodecType.h264,
            AVVideoWidthKey: width, AVVideoHeightKey: height,
            AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: 16_000_000, AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel],
        ]
        input = AVAssetWriterInput(mediaType: .video, outputSettings: settings)
        input.expectsMediaDataInRealTime = true
        writer.add(input)
        super.init()
    }

    func stream(_ stream: SCStream, didOutputSampleBuffer sb: CMSampleBuffer, of type: SCStreamOutputType) {
        guard type == .screen, sb.isValid else { return }
        // Only frames that carry new content ("complete") are written.
        guard let atts = CMSampleBufferGetSampleAttachmentsArray(sb, createIfNecessary: false) as? [[SCStreamFrameInfo: Any]],
              let raw = atts.first?[.status] as? Int, let status = SCFrameStatus(rawValue: raw), status == .complete else { return }
        lock.lock(); defer { lock.unlock() }
        if !started {
            writer.startWriting()
            writer.startSession(atSourceTime: CMSampleBufferGetPresentationTimeStamp(sb))
            started = true
        }
        if input.isReadyForMoreMediaData { input.append(sb); frames += 1 }
    }

    func stream(_ stream: SCStream, didStopWithError error: Error) {
        fputs("stream stopped: \(error)\n", stderr)
    }

    func finish() async {
        lock.lock(); input.markAsFinished(); lock.unlock()
        await writer.finishWriting()
    }
}

@main
struct Main {
    static func main() async {
        let a = CommandLine.arguments
        guard a.count >= 4, let pid = Int32(a[1]), let seconds = Double(a[2]) else {
            fputs("usage: WindowRecorder <pid> <seconds> <out.mp4> [fps]\n", stderr); exit(2)
        }
        let fps = a.count > 4 ? (Int32(a[4]) ?? 30) : 30
        _ = await MainActor.run { NSApplication.shared }   // a window-server connection, which capture needs
        do {
            let content = try await SCShareableContent.excludingDesktopWindows(false, onScreenWindowsOnly: false)
            let mine = content.windows.filter { $0.owningApplication?.processID == pid && ($0.title ?? "").contains("Minecraft") }
            guard let win = mine.max(by: { $0.frame.width * $0.frame.height < $1.frame.width * $1.frame.height }) else {
                fputs("no Minecraft window owned by pid \(pid); refusing to record anything else\n", stderr); exit(3)
            }
            print("recording window \(win.windowID) '\(win.title ?? "")' \(Int(win.frame.width))x\(Int(win.frame.height)) pt")
            let filter = SCContentFilter(desktopIndependentWindow: win)
            let cfg = SCStreamConfiguration()
            let scale = CGFloat(filter.pointPixelScale)
            let w = Int(win.frame.width * scale) & ~1, h = Int(win.frame.height * scale) & ~1
            cfg.width = w; cfg.height = h
            cfg.minimumFrameInterval = CMTime(value: 1, timescale: fps)
            cfg.showsCursor = false
            cfg.pixelFormat = kCVPixelFormatType_32BGRA
            cfg.queueDepth = 8
            let rec = try Recorder(url: URL(fileURLWithPath: a[3]), width: w, height: h)
            let stream = SCStream(filter: filter, configuration: cfg, delegate: rec)
            try stream.addStreamOutput(rec, type: .screen, sampleHandlerQueue: DispatchQueue(label: "frames"))
            try await stream.startCapture()
            try await Task.sleep(nanoseconds: UInt64(seconds * 1_000_000_000))
            try await stream.stopCapture()
            await rec.finish()
            print("wrote \(rec.frames) frames, \(w)x\(h), to \(a[3])")
        } catch {
            fputs("error: \(error)\n", stderr); exit(1)
        }
    }
}
