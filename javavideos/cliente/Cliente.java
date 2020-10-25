package cliente;

import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.net.DatagramPacket;
import java.net.InetAddress;
import java.net.MulticastSocket;
import java.util.Scanner;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class Cliente {
	static int port = 50005;
	static JButton b1;

	public static void main(String args[]) throws Exception
	{
		String[] grupos = {"225.1.2.3", "225.2.3.4", "225.3.4.5"};
		while (true)
		{
			System.out.println("Escriba el canal al que desea conectarse(1,2,3)");
			Scanner lectorConsola = new Scanner(System.in);
			int canal = lectorConsola.nextInt(); 

			System.setProperty("java.net.preferIPv4Stack", "true");

			InetAddress group = InetAddress.getByName(grupos[canal-1]);
			MulticastSocket mSocket = new MulticastSocket(port);
			mSocket.setReuseAddress(true);
			mSocket.joinGroup(group);

			//	        DatagramSocket serverSocket = new DatagramSocket(port);

			/**
			 * Formula for lag = (byte_size/sample_rate)*2
			 * Byte size 9728 will produce ~ 0.45 seconds of lag. Voice slightly broken.
			 * Byte size 1400 will produce ~ 0.06 seconds of lag. Voice extremely broken.
			 * Byte size 4000 will produce ~ 0.18 seconds of lag. Voice slightly more broken then 9728.
			 */

			System.out.println("Conectado");


			JFrame jframe = new JFrame("Canal "+canal);
			jframe.setSize(880,500);
			jframe.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			JLabel vidpanel = new JLabel();
			jframe.getContentPane().add(vidpanel);
			jframe.setVisible(true);

			byte[] receiveData = new byte[65500];

			DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
			b1 = new JButton("Stop");
			b1.addActionListener(new ActionListener()
		    {
		      public void actionPerformed(ActionEvent e)
		      {
		        b1.setText("ACABO");
		      }
		    });
			jframe.getContentPane().add(b1, BorderLayout.SOUTH);
			while (b1.getText()!= "ACABO")
			{
				mSocket.receive(receivePacket);
				byte[] recv = receivePacket.getData();
				ByteArrayInputStream bas = new ByteArrayInputStream(recv);
				
				BufferedImage bi=ImageIO.read(bas);
				ImageIcon image =  new ImageIcon(bi);
				vidpanel.setIcon(image);
				vidpanel.repaint();
			}
			jframe.setVisible(false);
		}
		
	}
}