import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers
let paths=CommandLine.arguments.dropFirst().map{String($0)}
for page in 0..<((paths.count+5)/6){let ctx=CGContext(data:nil,width:1600,height:1350,bitsPerComponent:8,bytesPerRow:6400,space:CGColorSpaceCreateDeviceRGB(),bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue)!;ctx.setFillColor(CGColor(gray:0.93,alpha:1));ctx.fill(CGRect(x:0,y:0,width:1600,height:1350));for j in 0..<6 {let k=page*6+j;if k>=paths.count{break};let src=CGImageSourceCreateWithURL(URL(fileURLWithPath:paths[k]) as CFURL,nil)!;let img=CGImageSourceCreateImageAtIndex(src,0,nil)!;ctx.draw(img,in:CGRect(x:(j%2)*800,y:1350-(j/2+1)*450,width:800,height:450))};let url=URL(fileURLWithPath:".context/visual-qa-01-02/montage-\(page+1).png");let dest=CGImageDestinationCreateWithURL(url as CFURL,UTType.png.identifier as CFString,1,nil)!;CGImageDestinationAddImage(dest,ctx.makeImage()!,nil);CGImageDestinationFinalize(dest)}
