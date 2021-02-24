import datetime
from BaseXClient import BaseXClient

session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')


def comment(local_id):
    comments = [
        {"name": "Roberto Suben", "comment": "Preferia ver Sol 30 vezes a ter isto", "date": "2020-12-09", "id": "0"},
        {"name": "GilBerto Verde", "comment": "AAAADDDDOORREEEEIIII S2", "date": "2020-12-09", "id": "1"},
        {"name": "Maria Cantil", "comment": "Meh!", "date": "2020-12-09", "id": "2"},
        {"name": "Roberto Suben", "comment": "Preferia ver Sol 30 vezes a ter isto", "date": "2020-12-09", "id": "3"},
        {"name": "GilBerto Verde", "comment": "AAAADDDDOORREEEEIIIIAAAADDDDOORREEEEIIIIAAAADDDDOORREEEEIIII S2",
         "date": "2020-12-09", "id": "4"},
        {"name": "Maria Cantil", "comment": "Meh!", "date": "2020-12-09", "id": "5"},
        {"name": "Roberto Suben", "comment": "Preferia ver Sol 30 vezes a ter isto", "date": "2020-12-09", "id": "6"},
        {"name": "GilBerto Verde", "comment": "AAAADDDDOORREEEEIIII S2", "date": "2020-12-09", "id": "7"},
        {"name": "Maria Cantil", "comment": "Meh!", "date": "2020-12-09", "id": "8"}]

    def_local_id = 2742611 # Aveiro
    query = f'''  
    import module namespace c = "FiveDayForecast.functions";

    c:list_comments({local_id})
                '''
    query2 = session.query(query)
    xml = query2.execute()

    root = etree.XML(xml)



    date = str(datetime.date.today())
    comments_str = f'''
            <div>
                <div class="card">
                    <div class="card-body overflow-auto" style="max-height: 600px">
                        <h4 class="card-title d-flex justify-content-between align-items-center">
                        Comments
                        </h4>
                        <form class="form-floating">
                            <div class="row g-2">
                            <div class="col-10">
                                <input type="text" class="form-control" placeholder="Name">
                            </div>
                            <div class="col-2">
                                <input type="date" class="form-control" value="{date}" readonly="True"></input>
                            </div>
                            <div class="col-12 mb-4">
                                <textarea type="text" class="form-control" style="max-width: 100%;" placeholder="Comment" spellcheck="True"></textarea>
                            </div>
                            <div class="col mb-4">
                                <button class="btn btn-primary" type="submit">Submit</button>
                            </div>
                            </div>
                        </form>
                        <div class="card-block">
                             <div class="row">
                '''
    for r in comments:
        comments_str += f'''
                                <div class="col-md-6 mb-4" id="{r["id"]}">
                                    <div class= "card">
                                        <div class="card-body">
                                            <div class="clearfix"">
                                                <h5 class="float-left">{r["name"]}</h5> 
                                                <span class="float-right">
                                                    <input type="date" class="form-control" value="{r["date"]}" readonly="True"></input>
                                                </span>
                                            </div>
                                            <p>{r["comment"]}</p>
                                        </div>
                                        <div class="card-footer">
                                            <button type="button" class="btn btn-danger btn-sm btn-block" id="{r["id"]}">Remove</button>
                                        </div>
                                    </div>
                            </div>
                        '''
    comments_str += '''         
                             </div>
                        </div>
                    </div>
                </div>
            </div>
                '''
    return comments_str

def new_comment(local_id, name, data, date):

    return
