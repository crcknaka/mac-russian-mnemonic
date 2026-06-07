// Generate an .iconset (PNGs at all required sizes) for the layout icon.
// Draws a white "RU" on a gray rounded-square, matching the native macOS
// input-source badge. Usage: swift make_icon.swift <iconset-dir>
import AppKit

let args = CommandLine.arguments
let outDir = args.count > 1 ? args[1] : "Icon.iconset"
try? FileManager.default.createDirectory(atPath: outDir, withIntermediateDirectories: true)

func makeIcon(pixels: Int, to path: String) {
    let s = CGFloat(pixels)
    guard let rep = NSBitmapImageRep(
        bitmapDataPlanes: nil, pixelsWide: pixels, pixelsHigh: pixels,
        bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
        colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0) else { return }
    rep.size = NSSize(width: s, height: s)

    NSGraphicsContext.saveGraphicsState()
    let ctx = NSGraphicsContext(bitmapImageRep: rep)!
    NSGraphicsContext.current = ctx

    // Rounded-square background matching the original macOS input-source
    // badge color. The badge fills the canvas like the system icons.
    let inset = s * 0.045
    let rect = CGRect(x: inset, y: inset, width: s - 2*inset, height: s - 2*inset)
    let radius = s * 0.16
    let bg = NSBezierPath(roundedRect: rect, xRadius: radius, yRadius: radius)
    NSColor(srgbRed: 0.131, green: 0.129, blue: 0.125, alpha: 1.0).setFill()
    bg.fill()

    // Centered white "RU".
    let letter = "RU" as NSString
    let font = NSFont.systemFont(ofSize: s * 0.40, weight: .bold)
    let para = NSMutableParagraphStyle(); para.alignment = .center
    let attrs: [NSAttributedString.Key: Any] = [
        .font: font, .foregroundColor: NSColor.white, .paragraphStyle: para,
    ]
    let tsize = letter.size(withAttributes: attrs)
    let pt = NSPoint(x: (s - tsize.width)/2, y: (s - tsize.height)/2 + s*0.005)
    letter.draw(at: pt, withAttributes: attrs)

    NSGraphicsContext.restoreGraphicsState()

    guard let png = rep.representation(using: .png, properties: [:]) else { return }
    try? png.write(to: URL(fileURLWithPath: path))
}

let items: [(Int, String)] = [
    (16, "icon_16x16.png"),   (32, "icon_16x16@2x.png"),
    (32, "icon_32x32.png"),   (64, "icon_32x32@2x.png"),
    (128, "icon_128x128.png"),(256, "icon_128x128@2x.png"),
    (256, "icon_256x256.png"),(512, "icon_256x256@2x.png"),
    (512, "icon_512x512.png"),(1024, "icon_512x512@2x.png"),
]
for (px, name) in items { makeIcon(pixels: px, to: "\(outDir)/\(name)") }
print("wrote \(items.count) PNGs to \(outDir)")
