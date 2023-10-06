import functools
import logging

from ..core.clients import postgres, airtable
from ..core.types import concepts, env_types


class IndividualViewSyncer:

    def __init__(self, replication: env_types.Replication, pg_table: concepts.Table | concepts.TableId):
        self.replication = replication

        if not isinstance(pg_table, concepts.Table):
            self.pg_table = next(
                (
                    table for table in postgres.Client(self.replication.schema_name).get_schema()
                    if table.id == pg_table
                ),
                None
            )

        else:
            self.pg_table = pg_table

    @functools.cached_property
    def logger(self) -> logging.Logger:
        return logging.getLogger('Schema Syncer')

    @functools.cached_property
    def airtable_table(self) -> concepts.Table:
        self.logger.debug('Getting schema from Airtable')

        return next(
            (table for table in airtable.Client(self.replication.base_id).get_schema() if table.id == self.pg_table.id),
            None
        )

    def drop_view(self) -> None:
        self.logger.info(f'Dropping view {self.pg_table.name}')
        postgres.Client(self.replication.schema_name).drop_view(self.pg_table)

    def create_view(self) -> None:
        self.logger.info(f'Creating view {self.pg_table.name}')
        db_table_fields = {field.id for field in self.pg_table.fields}
        airtable_table_restricted_to_current_db_columns = concepts.Table(
            id=self.pg_table.id,
            name=self.airtable_table.name,
            fields=[field for field in self.airtable_table.fields if field.id in db_table_fields],
        )
        postgres.Client(self.replication.schema_name).create_view(
            table=airtable_table_restricted_to_current_db_columns
        )
        postgres.Client(self.replication.schema_name).update_table_name(table=self.airtable_table)

    def sync(self) -> None:
        self.logger.info(f'Syncing view {self.airtable_table.name}')
        self.drop_view()
        self.create_view()

# check how the change handler would handle a name change
