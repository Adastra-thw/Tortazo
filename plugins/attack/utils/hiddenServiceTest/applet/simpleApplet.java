import javax.swing.JApplet;
import java.awt.*;
import javax.swing.JApplet;
import java.awt.Graphics;
import java.net.NetworkInterface;
import java.net.InterfaceAddress;
import java.net.InetAddress;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;
import java.util.Enumeration;
import java.nio.*;
import java.io.DataOutputStream;

public class simpleApplet {//extends JApplet{
   public void paint(Graphics g){
        StringBuffer cliente = new StringBuffer();
		int direccionDetectada = 1;
		try{
		    Enumeration e = NetworkInterface.getNetworkInterfaces();
		    while(e.hasMoreElements()) {
				NetworkInterface ni = (NetworkInterface) e.nextElement();
				cliente.append("INTERFAZ DE RED DETECTADA, Inicio de Traza...");
				cliente.append("\nDIRECCIÓN DETECTADA NÚMERO: "+direccionDetectada);
				cliente.append("\nNet interface: "+ni.getName());
				cliente.append("\nMAC: "+ni.getHardwareAddress()+"");
				cliente.append("\nMTU: "+ni.getMTU());
				cliente.append("\nPoint to Point? "+ni.getMTU());
				cliente.append("\nes UP? "+ni.isUp());
				cliente.append("\nes Virtual? "+ni.isVirtual());
				cliente.append("\nSoporta Multicast? "+ni.supportsMulticast() );
				List<InterfaceAddress> subSetIface = ni.getInterfaceAddresses();
				for(InterfaceAddress interfaceAddress : subSetIface) {
					cliente.append("\n --- BROADCAST: "+interfaceAddress.getBroadcast());
					cliente.append("\n --- MASCARA DE SUBRED "+interfaceAddress.getNetworkPrefixLength());
				}
				cliente.append("\nFin de Traza...\n\n\n");
			}
		}catch(Exception exc ){
		    exc.printStackTrace();
		}
      //g.drawString("Hello"+cliente.toString(),400,200);
      System.out.println(cliente.toString());
   }

   public static void main(String ... args) {

        StringBuffer cliente = new StringBuffer();
		int direccionDetectada = 1;
		try{
		    Enumeration e = NetworkInterface.getNetworkInterfaces();
		    while(e.hasMoreElements()) {
				NetworkInterface ni = (NetworkInterface) e.nextElement();
				cliente.append("INTERFAZ DE RED DETECTADA, Inicio de Traza...");
				cliente.append("\nDIRECCIÓN DETECTADA NÚMERO: "+direccionDetectada);
				cliente.append("\nNet interface: "+ni.getName());
				cliente.append("\nMAC: "+ni.getHardwareAddress()+"");
				cliente.append("\nMTU: "+ni.getMTU());
				cliente.append("\nPoint to Point? "+ni.getMTU());
				cliente.append("\nes UP? "+ni.isUp());
				cliente.append("\nes Virtual? "+ni.isVirtual());
				cliente.append("\nSoporta Multicast? "+ni.supportsMulticast() );
				List<InterfaceAddress> subSetIface = ni.getInterfaceAddresses();
				for(InterfaceAddress interfaceAddress : subSetIface) {
					cliente.append("\n --- BROADCAST: "+interfaceAddress.getBroadcast());
					cliente.append("\n --- MASCARA DE SUBRED "+interfaceAddress.getNetworkPrefixLength());
				}
				cliente.append("\nFin de Traza...\n\n\n");
			}
		}catch(Exception exc ){
		    exc.printStackTrace();
		}
        System.out.println(cliente.toString());

   }
}


