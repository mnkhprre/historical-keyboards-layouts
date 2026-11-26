// Renders a short text glyph into a keyboard-layout .icns (black glyph, transparent background).
// Usage: swift scripts/make-icon.swift "<text>" "<font name>" <output.icns>
import AppKit

let args = CommandLine.arguments
guard args.count == 4 else {
    FileHandle.standardError.write("usage: make-icon.swift <text> <font> <out.icns>\n".data(using: .utf8)!)
    exit(2)
}
let text = args[1], fontName = args[2], out = URL(fileURLWithPath: args[3])

let iconset = FileManager.default.temporaryDirectory
    .appendingPathComponent(UUID().uuidString + ".iconset")
try FileManager.default.createDirectory(at: iconset, withIntermediateDirectories: true)

func render(_ px: Int) -> Data {
    let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: px, pixelsHigh: px,
                               bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
                               colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
    var size = CGFloat(px) * 0.9
    var attrs: [NSAttributedString.Key: Any] = [:]
    var bounds = NSRect.zero
    // Shrink until the glyph fits with a small margin.
    repeat {
        let font = NSFont(name: fontName, size: size) ?? NSFont.systemFont(ofSize: size, weight: .semibold)
        attrs = [.font: font, .foregroundColor: NSColor.black]
        bounds = (text as NSString).boundingRect(with: .zero, options: [.usesLineFragmentOrigin], attributes: attrs)
        size *= 0.95
    } while (bounds.width > CGFloat(px) * 0.94 || bounds.height > CGFloat(px) * 1.1) && size > 4
    let origin = NSPoint(x: (CGFloat(px) - bounds.width) / 2, y: (CGFloat(px) - bounds.height) / 2)
    (text as NSString).draw(at: origin, withAttributes: attrs)
    NSGraphicsContext.restoreGraphicsState()
    return rep.representation(using: .png, properties: [:])!
}

for base in [16, 32, 128, 256, 512] {
    try render(base).write(to: iconset.appendingPathComponent("icon_\(base)x\(base).png"))
    try render(base * 2).write(to: iconset.appendingPathComponent("icon_\(base)x\(base)@2x.png"))
}
let p = Process()
p.executableURL = URL(fileURLWithPath: "/usr/bin/iconutil")
p.arguments = ["-c", "icns", iconset.path, "-o", out.path]
try p.run(); p.waitUntilExit()
try? FileManager.default.removeItem(at: iconset)
exit(p.terminationStatus)
