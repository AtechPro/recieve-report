    def detailed_picture(self):
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        col_widths = [140, 50]  # Two columns: ITEM (wide), DESCRIPTION OF SERVICES (narrow)
        line_height = 3
        image_height = 35

        grey = (128, 128, 128)
        headings_style = FontFace(emphasis="B", fill_color=grey)
        # Table header (full width)
        with self.table(col_widths=col_widths, line_height=4, headings_style=headings_style) as table:
            row = table.row()
            row.cell('DETAILS PICTURE OF SERVICED ITEM', align='C', colspan=2)

        # Section header row (drawn manually for perfect alignment)
        x_start = self.l_margin
        y_start = self.get_y()
        self.set_xy(x_start, y_start)
        self.set_font(self.FONT_FAMILY, 'B', self.FONT_SIZE)
        self.cell(col_widths[0], line_height * 2, 'ITEM:', border=1, align='C')
        self.cell(col_widths[1], line_height * 2, 'DESCRIPTION OF SERVICES', border=1, align='C')
        self.ln(line_height * 2)
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)

        detailed_pictures = self.valve_data.get('detailed_pictures', [])
        for i, picture_data in enumerate(detailed_pictures):
            proposed_action = picture_data.get('proposed_action', '')
            image_path_1 = picture_data.get('image_path_1', '')
            image_path_2 = picture_data.get('image_path_2', '')

            # Calculate required height for each cell
            y_start = self.get_y()
            x_start = self.l_margin
            self.set_xy(x_start, y_start)
            action_height = self.get_string_height(col_widths[1], proposed_action, line_height)
            row_height = max(action_height, image_height)

            # Page break if needed
            if self.get_y() + row_height > self.page_break_trigger:
                self.add_page()
                y_start = self.get_y()

            # Draw ITEM cell (first column, for images)
            self.set_xy(x_start, y_start)
            self.cell(col_widths[0], row_height, '', border=1)
            # Draw images if any
            image_x = x_start + 2
            image_y = y_start + 2
            uploaded_images = []
            if image_path_1 and image_path_1 != 'goodvalve.png' and os.path.exists(image_path_1):
                uploaded_images.append(image_path_1)
            if image_path_2 and image_path_2 != 'goodvalve.png' and os.path.exists(image_path_2):
                uploaded_images.append(image_path_2)
            for idx, img_path in enumerate(uploaded_images):
                if idx == 0:
                    self.image(img_path, x=image_x, y=image_y, w=60, h=30)
                elif idx == 1:
                    self.image(img_path, x=image_x + 65, y=image_y, w=60, h=30)

            # Draw DESCRIPTION OF SERVICES cell (second column)
            self.set_xy(x_start + col_widths[0], y_start)
            self.multi_cell(col_widths[1], line_height, proposed_action, border=0, align='L')
            y_after_action = self.get_y()
            if y_after_action < y_start + row_height:
                self.set_xy(x_start + col_widths[0], y_after_action)
                self.cell(col_widths[1], y_start + row_height - y_after_action, '', border=0)
            self.rect(x_start + col_widths[0], y_start, col_widths[1], row_height)

            # Move to the start of the next row
            self.set_y(y_start + row_height)

    def get_string_height(self, w, txt, line_height):
        # Helper to calculate the height a multicell would take
        if not txt:
            return line_height
        # Split by newlines first
        lines = txt.split('\n')
        total_lines = 0
        for line in lines:
            # Estimate number of lines for this chunk
            str_width = self.get_string_width(line)
            n_lines = max(1, int(str_width / w) + 1)
            total_lines += n_lines
        return total_lines * line_height