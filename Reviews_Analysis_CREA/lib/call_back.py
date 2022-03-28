from bokeh.models import CustomJS



# handle the currently selected article
def selected_code():
    code = """
            var username = [];
            var review = [];
            var score = [];
            cb_data.source.selected.indices.forEach(index => username.push(source.data['username'][index]));
            cb_data.source.selected.indices.forEach(index => review.push(source.data['review'][index]));
            cb_data.source.selected.indices.forEach(index => score.push(source.data['score'][index]));
            username = "<p1><b>username</b> " + username[0].toString().replace(/<br>/g, ' ') + "<br>"
            review = "<p1><b>review</b> " + review[0].toString().replace(/<br>/g, ' ') + "<br>"
            score = "<p1><b>score</b> " + score[0].toString().replace(/<br>/g, ' ') + "<br>"
            current_selection.text = username + review + score
            current_selection.change.emit();
    """
    return code

# handle the keywords and search
def input_callback(plot, source, out_text, topics):

    # slider call back for cluster selection
    callback = CustomJS(args=dict(p=plot, source=source, out_text=out_text, topics=topics), code="""
                				var key = text.value;
                				key = key.toLowerCase();
                				var cluster = slider.value;
                var data = source.data;


                x = data['x'];
                y = data['y'];
                x_backup = data['x_backup'];
                y_backup = data['y_backup'];
                labels = data['desc'];
                username = data['username'];
                review = data['review'];
                score = data['score'];
                if (cluster == '20') {
                    out_text.text = 'Keywords: Slide to specific cluster to see the keywords.';
                    for (i = 0; i < x.length; i++) {
                        						if(username[i].includes(key) ||
                        						review[i].includes(key) ||
                        						score[i].includes(key)) {
                        							x[i] = x_backup[i];
                        							y[i] = y_backup[i];
                        						} else {
                        							x[i] = undefined;
                        							y[i] = undefined;
                        						}
                    }
                }
                else {
                    out_text.text = 'Keywords: ' + topics[Number(cluster)];
                    for (i = 0; i < x.length; i++) {
                        if(labels[i] == cluster) {
                            							if(username[i].includes(key) ||
                            							review[i].includes(key) ||
                            							score[i].includes(key)) {
                            								x[i] = x_backup[i];
                            								y[i] = y_backup[i];
                            							} else {
                            								x[i] = undefined;
                            								y[i] = undefined;
                            							}
                        } else {
                            x[i] = undefined;
                            y[i] = undefined;
                        }
                    }
                }
            source.change.emit();
            """)
    return callback
