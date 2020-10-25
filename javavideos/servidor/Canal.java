package servidor;

import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.InetAddress;
import java.net.MulticastSocket;
import java.net.SocketException;
import java.net.UnknownHostException;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.MatOfByte;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.videoio.VideoCapture;

public class Canal implements Runnable {
	private String ruta;
	private int canal;
	private String grupo;

	public Canal(String pRuta, int pCanal, String pGrupo) {
		this.ruta = pRuta;
		this.canal = pCanal;
		this.grupo = pGrupo;
	}

	public void run() {
		try {
			System.setProperty("java.net.preferIPv4Stack", "true");

			DatagramPacket dgp;
			InetAddress address;
			int puerto = 50005;
			System.out.println("Inicio del canal " + canal);


			System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
			Mat frame = new Mat();
			VideoCapture videoCap = new VideoCapture(this.ruta);
			JFrame jframe = new JFrame("SERVER: canal "+ this.canal);
			jframe.setSize(880,500);


			jframe.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			JLabel videoLabel = new JLabel();
			jframe.setContentPane(videoLabel);
			jframe.setVisible(true);


			byte[] data = new byte[65500];

			address = InetAddress.getByName(this.grupo);
			MulticastSocket socket = new MulticastSocket();

			while (true) {
				if (videoCap.read(frame)) {
					MatOfByte mob=new MatOfByte();
					Imgcodecs.imencode(".jpg", frame, mob);
					byte bytes[]=mob.toArray();
					ByteArrayInputStream byteA = new ByteArrayInputStream(bytes);


					byteA.read(data, 0, data.length);
					ByteArrayInputStream byteArray2 = new ByteArrayInputStream(data);

					BufferedImage bufferedImg = ImageIO.read(byteArray2);
					ImageIcon image =  new ImageIcon(bufferedImg);
					videoLabel.setIcon(image);
					videoLabel.repaint();


					dgp = new DatagramPacket (data,data.length, address, puerto);
					socket.send(dgp);
				}
				else {
					videoCap = new VideoCapture(this.ruta);
				}
			}
		}

		catch (UnknownHostException e) {
			System.out.println(e);
		} catch (SocketException e1) {
			System.out.println(e1);
		} catch (IOException e2) {
			System.out.println(e2);
		}
	}

	static BufferedImage Mat2BufferedImage(Mat matrix)throws Exception {        
		MatOfByte mob = new MatOfByte();
		Imgcodecs.imencode(".jpg", matrix, mob);
		byte bytes[] = mob.toArray();

		BufferedImage bufferedImg = ImageIO.read(new ByteArrayInputStream(bytes));
		return bufferedImg;
	}

}