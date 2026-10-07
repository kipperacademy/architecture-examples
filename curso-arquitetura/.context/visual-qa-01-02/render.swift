import Foundation
import CoreGraphics
import CoreText
import ImageIO
import UniformTypeIdentifiers
class Renderer:NSObject,XMLParserDelegate {
 let ctx:CGContext
 var inText=false,text="", attrs:[String:String]=[:],inDefs=false
 init(_ c:CGContext){ctx=c}
 func col(_ s:String)->CGColor {let n=Int(s.trimmingCharacters(in:CharacterSet(charactersIn:"#")),radix:16) ?? 0;return CGColor(red:CGFloat((n>>16)&255)/255,green:CGFloat((n>>8)&255)/255,blue:CGFloat(n&255)/255,alpha:1)}
 func num(_ a:[String:String],_ k:String)->CGFloat {CGFloat(Double(a[k] ?? "0") ?? 0)}
 func parser(_ p:XMLParser,didStartElement e:String,namespaceURI:String?,qualifiedName:String?,attributes a:[String:String]){
 if e=="defs"{inDefs=true};if inDefs{return}
 if e=="rect"{let path=CGPath(roundedRect:CGRect(x:num(a,"x"),y:900-num(a,"y")-num(a,"height"),width:num(a,"width"),height:num(a,"height")),cornerWidth:14,cornerHeight:14,transform:nil);ctx.addPath(path);ctx.setFillColor(col(a["fill"] ?? "#ffffff"));ctx.setStrokeColor(col(a["stroke"] ?? "#000000"));ctx.setLineWidth(2);ctx.drawPath(using:.fillStroke)}
 if e=="text"{inText=true;text="";attrs=a}
 if e=="path",let d=a["d"]{let v=d.replacingOccurrences(of:"M",with:"").replacingOccurrences(of:"L",with:" ").split(separator:" ").compactMap{Double($0)};if v.count==4{let x=v[0],y=900-v[1],x2=v[2],y2=900-v[3];ctx.setStrokeColor(col(a["stroke"] ?? "#9c36b5"));ctx.setLineWidth(3);ctx.move(to:CGPoint(x:x,y:y));ctx.addLine(to:CGPoint(x:x2,y:y2));ctx.strokePath();let angle=atan2(y2-y,x2-x);ctx.move(to:CGPoint(x:x2-15*cos(angle-0.4),y:y2-15*sin(angle-0.4)));ctx.addLine(to:CGPoint(x:x2,y:y2));ctx.addLine(to:CGPoint(x:x2-15*cos(angle+0.4),y:y2-15*sin(angle+0.4)));ctx.strokePath()}}
 }
 func parser(_ p:XMLParser,foundCharacters s:String){if inText{text+=s}}
 func parser(_ p:XMLParser,didEndElement e:String,namespaceURI:String?,qualifiedName:String?){if e=="defs"{inDefs=false};if e=="text"{let font=CTFontCreateWithName((attrs["font-family"]?.contains("monospace") == true ? "Courier New" : "Arial") as CFString,num(attrs,"font-size"),nil);let a=NSAttributedString(string:text,attributes:[NSAttributedString.Key(kCTFontAttributeName as String):font,NSAttributedString.Key(kCTForegroundColorAttributeName as String):col(attrs["fill"] ?? "#000000")]);ctx.textPosition=CGPoint(x:num(attrs,"x"),y:900-num(attrs,"y"));CTLineDraw(CTLineCreateWithAttributedString(a),ctx);inText=false}}
}
for arg in CommandLine.arguments.dropFirst(){let url=URL(fileURLWithPath:arg);let context=CGContext(data:nil,width:1600,height:900,bitsPerComponent:8,bytesPerRow:6400,space:CGColorSpaceCreateDeviceRGB(),bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue)!;let parser=XMLParser(contentsOf:url)!;let renderer=Renderer(context);parser.delegate=renderer;assert(parser.parse());let out=".context/visual-qa-01-02/"+url.pathComponents[url.pathComponents.count-3].prefix(2)+"-"+url.lastPathComponent+".png";let dest=CGImageDestinationCreateWithURL(URL(fileURLWithPath:out) as CFURL,UTType.png.identifier as CFString,1,nil)!;CGImageDestinationAddImage(dest,context.makeImage()!,nil);assert(CGImageDestinationFinalize(dest));print(out)}
