#include <gtk/gtk.h>
#include <cstdlib>

/*
struct restart_data
{
	GObject *window;
	bool conf;
};
*/

void show_widget(GtkWidget *widget, gpointer data);
void hide_widget(GtkWidget *widget, gpointer data);
void launch_kodi();
void fix_net();
void restart_dialogue(GtkWidget *widget, gpointer data);
void restart_dev();
void check_updates();

int main(int argc, char **argv)
{
	GtkBuilder *builder;

   // main window
   GObject *main, *box, *menu, *title, *kodi, *net, *restart, *update;
   // menu bar
   GObject *menu_file, *menu_help, *sub_file, *sub_help, *menu_quit, *menu_about;
   // about window
   GObject *about, *about_box, *about_text, *license, *about_ok;
   // restart dialogue
   GObject *restart_win, *restart_box, *restart_bbox, *restart_ok,
           *restart_cancel, *restart_text;

	gtk_init(&argc, &argv);

	builder = gtk_builder_new();
	gtk_builder_add_from_file(builder, "main.ui", NULL);

	// main window
	main		= gtk_builder_get_object(builder, "main");
	box		= gtk_builder_get_object(builder, "box");
	menu		= gtk_builder_get_object(builder, "menu");
	title 	= gtk_builder_get_object(builder, "title");
	kodi		= gtk_builder_get_object(builder, "kodi");
	net 		= gtk_builder_get_object(builder, "net");
	restart	= gtk_builder_get_object(builder, "restart");
	update	= gtk_builder_get_object(builder, "update");

	// menu bar
	menu_file	= gtk_builder_get_object(builder, "menu_file");
	menu_help	= gtk_builder_get_object(builder, "menu_help");
	sub_file 	= gtk_builder_get_object(builder, "sub-file");
	menu_quit	= gtk_builder_get_object(builder, "menu-quit");
	sub_help		= gtk_builder_get_object(builder, "sub-help");
	menu_about	= gtk_builder_get_object(builder, "menu-about");

	// about window
	about			= gtk_builder_get_object(builder, "about");
	about_box	= gtk_builder_get_object(builder, "about-box");
	about_ok		= gtk_builder_get_object(builder, "about-ok");
	about_text  = gtk_builder_get_object(builder, "about-text");
	license		= gtk_builder_get_object(builder, "license");

	//restart window
	restart_win 	= gtk_builder_get_object(builder, "restart-win");
	restart_box 	= gtk_builder_get_object(builder, "restart-box");
	restart_bbox	= gtk_builder_get_object(builder, "restart-bbox");
	restart_ok		= gtk_builder_get_object(builder, "restart-ok");
	restart_cancel	= gtk_builder_get_object(builder, "restart-cancel");
	restart_text	= gtk_builder_get_object(builder, "restart-text");

	g_signal_connect(main, "destroy", G_CALLBACK(gtk_main_quit), NULL);
	g_signal_connect(menu_quit, "activate", G_CALLBACK(gtk_main_quit), NULL);
	g_signal_connect(menu_about, "activate", G_CALLBACK(show_widget), about);
	g_signal_connect(about, "destroy", G_CALLBACK(hide_widget), about); // this could be done in other ways

	// main buttons
	g_signal_connect(kodi, "clicked", G_CALLBACK(launch_kodi), NULL);
	g_signal_connect(net, "clicked", G_CALLBACK(fix_net), NULL);
	g_signal_connect(restart, "clicked", G_CALLBACK(restart_dialogue), restart_win);
	g_signal_connect(update, "clicked", G_CALLBACK(check_updates), NULL);

	// about button
	g_signal_connect(about_ok, "clicked", G_CALLBACK(hide_widget), about);

	// restart buttons
	g_signal_connect(restart_ok, "clicked", G_CALLBACK(restart_dev), NULL);
	g_signal_connect(restart_cancel, "clicked", G_CALLBACK(hide_widget), restart_win);

	gtk_main();

	return 0;
}

void show_widget(GtkWidget *widget, gpointer data)
{
	gtk_widget_show(GTK_WIDGET(data));
}

void hide_widget(GtkWidget *widget, gpointer data)
{
	gtk_widget_hide(GTK_WIDGET(data));
}

void launch_kodi()
{
	system("kodi");
}

void fix_net()
{
   system("echo 'not yet implemented'");
}

void restart_dialogue(GtkWidget *widget, gpointer data)
{
	gtk_widget_show(GTK_WIDGET(data));
}

void restart_dev()
{
   system("reboot");
}

void check_updates()
{
   system("sudo apt update && sudo apt upgrade");
}
