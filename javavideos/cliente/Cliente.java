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
			System.out.println("Escriba el canal al que desea conectarse donde:");
			System.out.println("1 -> 225.1.2.3 - 50005");
			System.out.println("2 -> 225.2.3.4 - 50005");
			System.out.println("3 -> 225.3.4.5 - 50005");

			Scanner lectorConsola = new Scanner(System.in);
			int canal = lectorConsola.nextInt(); 

			System.setProperty("java.net.preferIPv4Stack", "true");

			InetAddress group = InetAddress.getByName(grupos[canal-1]);
			MulticastSocket mSocket = new MulticastSocket(port);
			mSocket.setReuseAddress(true);
			mSocket.joinGroup(group);

			System.out.println("Conexión exitosa");

			JFrame jframe = new JFrame("Conexión al canal "+ canal);
			jframe.setSize(880,500);
			jframe.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			JLabel videoLabel = new JLabel();
			jframe.getContentPane().add(videoLabel);
			jframe.setVisible(true);

			byte[] receiveData = new byte[65500];

			DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
			b1 = new JButton("Stop");
			b1.addActionListener(new ActionListener(){
				public void actionPerformed(ActionEvent e)
				{
					b1.setText("Terminado");
				}
			});

			jframe.getContentPane().add(b1, BorderLayout.SOUTH);
			while (b1.getText()!= "Terminado"){
				mSocket.receive(receivePacket);
				byte[] recv = receivePacket.getData();
				ByteArrayInputStream byteArray = new ByteArrayInputStream(recv);

				BufferedImage bufferedImg = ImageIO.read(byteArray);
				ImageIcon image =  new ImageIcon(bufferedImg);
				videoLabel.setIcon(image);
				videoLabel.repaint();
			}
			jframe.setVisible(false);
		}

	}
}